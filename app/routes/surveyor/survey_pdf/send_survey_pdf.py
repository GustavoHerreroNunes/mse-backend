from flask import request, jsonify, current_app
from sqlalchemy import text
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
import json
import os

from app.services import Session
from . import survey_pdf_bp, logger
from app.utils.upload_pdf_to_drive import upload_report_to_drive
from .utils.clear_upload_folder_files import clear_upload_folder_files

@survey_pdf_bp.route('/survey/pdf', methods=['POST'])
def send_survey_pdf():
    try:
        data = request.form.get('data')
        logger.info(data)
        data = json.loads(data)
        logger.info(f"🔍 request.files keys: {list(request.files.keys())}")
        logger.info(f"🔍 request.form: {request.form}")

        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        current_session = Session()

        try:
            # Check if task exists
            checklist_exists = current_session.execute(
                text("SELECT id_demanda FROM tbl_status_pdf WHERE id_demanda = :id"),
                {"id": data.get("id_demanda")}
            ).fetchone()

            if not checklist_exists:
                return jsonify({"error": "Task not found"}), 404

            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            survey = current_session.execute(
                text("SELECT id_pasta_gd_demanda FROM tbl_demandas WHERE id_demanda = :id_demanda"),
                {"id_demanda": data.get("id_demanda")}
            ).fetchone()

            if not survey:
                return jsonify({"error": "Task not found"}), 404
            
            id_google_drive = survey[0]

            if not id_google_drive:
                return jsonify({"error": "Missing Google Drive Folder Id"}), 404

            print(f"ID Google Drive: {id_google_drive}")

            # Upload to Drive
            uploaded_url = upload_report_to_drive(file_path, id_google_drive)
            if not uploaded_url:
                return jsonify({'error': 'Failed to upload to Google Drive'}), 500

            # Update database
            result = current_session.execute(
                text("""
                    UPDATE tbl_status_pdf
                    SET url_path_pdf_signed = :url_path_pdf_signed
                    WHERE id_demanda = :id_demanda
                    RETURNING id_demanda
                """),
                {
                    "url_path_pdf_signed": uploaded_url,
                    "id_demanda": data.get("id_demanda")
                }
            ).fetchone()

            current_session.commit()

            return jsonify({
                "message": "File added successfully",
                "id_demanda": result[0] if result else None
            }), 201

        except Exception as e:
            current_session.rollback()
            logger.error(f"Error adding photo: {str(e)}")
            return jsonify({"error": str(e)}), 500

        finally:
            current_session.close()
            clear_upload_folder_files()

    except ValidationError as e:
        return jsonify({"error": "Validation Error.", "details": e.messages}), 400
