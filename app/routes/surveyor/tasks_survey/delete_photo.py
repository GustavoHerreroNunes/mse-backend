from flask import jsonify
from sqlalchemy import text
from urllib.parse import urlparse, parse_qs

from app.services import Session
from . import tasks_survey_bp, logger
from app.utils.upload_image_drive import delete_file_from_drive

@tasks_survey_bp.route('/boarding/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    """Delete a photo by ID (DB + Google Drive)"""
    current_session = Session()

    try:
        result = current_session.execute(
            text("SELECT url_path FROM tbl_photo_survey_boarding WHERE id_photo = :id"),
            {"id": photo_id}
        )
        photo_record = result.fetchone()

        if not photo_record:
            return jsonify({"error": "Photo not found"}), 404

        url_path = photo_record._mapping['url_path']

        if url_path:
            try:
                # Log full URL for debugging
                logger.info(f"Processing URL: {url_path}")
                
                parsed_url = urlparse(url_path)
                query_params = parse_qs(parsed_url.query)
                file_id = query_params.get('id', [''])[0]

                logger.info(f"Extracted image id: {file_id}")

                
                success = delete_file_from_drive(file_id)
                if not success:
                    logger.warning(f"Failed to delete image {file_id} from Google Drive.")
            except Exception as e:
                logger.warning(f"Failed to process delete from Google Drive: {e}")
                

        current_session.execute(
            text("DELETE FROM tbl_photo_survey_boarding WHERE id_photo = :id"),
            {"id": photo_id}
        )
        current_session.commit()

        return jsonify({"message": "Photo deleted successfully"}), 200

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error deleting photo: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        current_session.close()