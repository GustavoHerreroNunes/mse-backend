from flask import request, jsonify, current_app
from sqlalchemy import text
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
import json
import os

from app.services import Session
from . import tasks_survey_bp, logger
from app.utils.upload_image_drive import allowed_file, upload_image_to_drive
from .utils.clear_upload_folder_files import clear_upload_folder_files

@tasks_survey_bp.route('/boarding/photos', methods=['POST'])
def add_photo():
    """Add new photos to a task (up to 6 images)"""
    try:
        data = request.form.get('data')
        
        if not data:
            return jsonify({"error": "Missing 'data' field in request"}), 400
        
        logger.info(f"Raw data: {data}")
        
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return jsonify({"error": "Invalid JSON format in 'data' field", "details": str(e)}), 400
        
        logger.info(f"🔍 request.files keys: {list(request.files.keys())}")
        logger.info(f"🔍 request.form: {request.form}")

        current_session = Session()

        try:
            # Check if task exists
            task = current_session.execute(
                text("SELECT id_task, id_survey FROM tbl_task_survey_boarding WHERE id_task = :id"),
                {"id": data.get("id_task")}
            )

            task_list = list(task.mappings().all())

            if not task_list:
                return jsonify({"error": "Task not found"}), 404
            
            id_demanda = task_list[0].get("id_survey", -1)
            if id_demanda == -1:
                return jsonify({"error": "Survey not found"}), 404
            
            print(f"ID Demanda: {id_demanda}")

            uploaded_photos = []

            for i in range(6):
                image_key = f'image_{i+1}'
                
                if image_key not in request.files:
                    continue

                image = request.files[image_key]

                if image.filename == '':
                    continue

                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)

                    survey = current_session.execute(
                        text("SELECT id_pasta_gd_demanda from tbl_demandas WHERE id_demanda = :id_demanda"),
                        {"id_demanda": id_demanda}
                    )

                    survey_list = list(survey.mappings().all())

                    if not survey_list:
                        return jsonify({"error": "Task not found"}), 404
                    
                    id_google_drive = survey_list[0].get("id_pasta_gd_demanda", -1)

                    if id_google_drive == -1:
                        return jsonify({"error": "Missing Google Drive Folder Id"}), 404

                    print(f"ID Google Drive: {id_google_drive}")

                    # Upload to Drive
                    uploaded_url = upload_image_to_drive(image_path, id_google_drive)
                    if not uploaded_url:
                        return jsonify({'error': f'Failed to upload {image_key} to Google Drive'}), 500

                    id_cargo = data.get("id_cargo") if data.get("id_cargo") != 0 else None
                    id_lifting_material = data.get("id_lifting_material") if data.get("id_lifting_material") != 0 else None
                    id_lashing_material = data.get("id_lashing_material") if data.get("id_lashing_material") != 0 else None

                    # Insert into database
                    result = current_session.execute(
                        text("""
                            INSERT INTO tbl_photo_survey_boarding (id_task, section_index, sub_section_index, url_path, id_cargo, id_lifting_material, id_lashing_material)
                            VALUES (:id_task, :section_index, :sub_section_index, :url_path, :id_cargo, :id_lifting_material, :id_lashing_material)
                            RETURNING id_photo
                        """),
                        {
                            "id_task": data.get("id_task"),
                            "section_index": data.get("section_index"),
                            "sub_section_index": data.get("sub_section_index"),
                            "url_path": uploaded_url,
                            "id_cargo": id_cargo,
                            "id_lifting_material": id_lifting_material,
                            "id_lashing_material": id_lashing_material
                        }
                    )
                    photo_id = result.fetchone()._mapping["id_photo"]
                    uploaded_photos.append({"id": photo_id, "image_url": uploaded_url})

            current_session.commit()

            if not uploaded_photos:
                return jsonify({"error": "No valid images uploaded"}), 400

            return jsonify({
                "message": "Photos added successfully",
                "photos": uploaded_photos
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