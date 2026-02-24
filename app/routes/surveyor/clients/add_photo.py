import os
import time
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import text

from . import clients_bp, logger
from app.services import Session

@clients_bp.route('/photo', methods=['POST'])
def add_client_photo():
    """Upload a single client photo and persist reference in tbl_photo_client."""
    
    from app.utils.upload_image_drive import allowed_file, upload_image_to_drive
    from app.routes.surveyor.tasks_survey.utils.clear_upload_folder_files import clear_upload_folder_files
    
    try:
        # Basic presence checks for file & fields before schema validation
        if 'image' not in request.files:
            return jsonify({"error": "Missing image file"}), 400
        image = request.files['image']
        if image.filename == '':
            return jsonify({"error": "Empty filename"}), 400
        if not allowed_file(image.filename):
            return jsonify({"error": "Invalid file type"}), 400

        # Extract and validate id_client
        id_client_raw = request.form.get('id_client')
        if id_client_raw is None:
            return jsonify({"error": "id_client is required"}), 400
        try:
            id_client_val = int(id_client_raw)
        except ValueError:
            return jsonify({"error": "id_client must be an integer"}), 400

        # Fetch customer name to derive client_sigla (first up to 4 letters, uppercase)
        current_session = Session()
        try:
            customer_row = current_session.execute(
                text("SELECT customer_name FROM tbl_customer WHERE customer_id = :cid"),
                {"cid": id_client_val},
            ).fetchone()
        except Exception as look_err:
            current_session.close()
            logger.error(f"Error looking up customer: {look_err}")
            return jsonify({"error": "Failed to lookup customer"}), 500

        if not customer_row:
            current_session.close()
            return jsonify({"error": "Client not found"}), 404
        
        customer_photo = current_session.execute(
            text("SELECT id_photo FROM tbl_photo_client WHERE id_client = :cid"),
            {"cid": id_client_val},
        ).fetchone()

        # Generate filename based on client name
        customer_name = customer_row._mapping["customer_name"] or "CLIENT"
        client_sigla = customer_name[:4].upper().replace(" ", "")
        ext = image.filename.rsplit('.', 1)[1].lower()
        safe_base = secure_filename(client_sigla)
        filename = f"{safe_base}_{int(time.time())}.{ext}"

        upload_folder = current_app.config.get('UPLOAD_FOLDER', '/tmp')
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

        uploaded_url = upload_image_to_drive(image_path, folder_id=None, is_client=True)
        if not uploaded_url:
            current_session.close()
            return jsonify({"error": "Failed to upload image to Google Drive"}), 500

        try:
            if customer_photo:
                # UPDATE existing photo
                photo_id = customer_photo._mapping["id_photo"]
                current_session.execute(
                    text(
                        """
                        UPDATE tbl_photo_client 
                        SET url_path = :url_path
                        WHERE id_client = :id_client
                        """
                    ),
                    {"id_client": id_client_val, "url_path": uploaded_url},
                )
                current_session.commit()
                message = "Client photo updated successfully"
                logger.info(f"Updated photo for client {id_client_val}")
            else:
                # INSERT new photo
                result = current_session.execute(
                    text(
                        """
                        INSERT INTO tbl_photo_client (id_client, url_path)
                        VALUES (:id_client, :url_path)
                        RETURNING id_photo
                        """
                    ),
                    {"id_client": id_client_val, "url_path": uploaded_url},
                )
                photo_id = result.fetchone()._mapping["id_photo"]
                current_session.commit()
                message = "Client photo uploaded successfully"
                logger.info(f"Created new photo for client {id_client_val}")
                
        except Exception as db_err:
            current_session.rollback()
            logger.error(f"DB operation failed for client photo: {db_err}")
            return jsonify({"error": "Database operation failed"}), 500

        return jsonify({
            "message": message,
            "client_sigla": client_sigla,
            "id_photo": photo_id,
            "image_url": uploaded_url,
        }), 201

    except Exception as e:
        logger.error(f"Error uploading client photo: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if current_session:
            current_session.close()
        clear_upload_folder_files()
