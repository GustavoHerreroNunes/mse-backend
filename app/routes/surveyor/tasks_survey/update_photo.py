from flask import request, jsonify, current_app
from sqlalchemy import text
import os
from werkzeug.utils import secure_filename

from app.services import Session
from . import tasks_survey_bp, logger
from app.utils.upload_image_drive import allowed_file, upload_image_to_drive, delete_file_from_drive
from .utils.clear_upload_folder_files import clear_upload_folder_files

@tasks_survey_bp.route('/boarding/photos/<int:photo_id>', methods=['PUT'])
def update_photo(photo_id):
    """Update an existing photo by replacing the image in Google Drive"""
    current_session = Session()

    try:
        # Fetch existing photo data
        result = current_session.execute(
            text("SELECT url_path FROM tbl_photo_survey_boarding WHERE id_photo = :id"),
            {"id": photo_id}
        )
        photo_record = result.fetchone()

        if not photo_record:
            return jsonify({"error": "Photo not found"}), 404

        old_url_path = photo_record._mapping['url_path']

        # Check if file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image = request.files['image']

        if image.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            # Upload new image to Google Drive
            new_url_path = upload_image_to_drive(image_path)
            if not new_url_path:
                return jsonify({'error': 'Failed to upload new image to Google Drive'}), 500

            # Delete old image from Google Drive (if exists)
            if old_url_path:
                try:
                    file_id = old_url_path.split("/d/")[1].split("/")[0]
                    success = delete_file_from_drive(file_id)
                    if not success:
                        logger.warning(f"Failed to delete old image {file_id} from Google Drive.")
                except Exception as delete_error:
                    logger.warning(f"Failed to process delete for old image: {delete_error}")

            # Update database record with new URL
            current_session.execute(
                text("""
                    UPDATE tbl_photo_survey_boarding 
                    SET url_path = :url_path
                    WHERE id_photo = :id
                """),
                {"url_path": new_url_path, "id": photo_id}
            )
            current_session.commit()

            return jsonify({
                "message": "Photo updated successfully",
                "image_url": new_url_path
            }), 200

        else:
            return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg'}), 400

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error updating photo: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        current_session.close()
        clear_upload_folder_files()