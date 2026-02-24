from urllib.parse import parse_qs, urlparse
from flask import jsonify
from sqlalchemy import text

from app.utils.upload_image_drive import delete_file_from_drive

from . import clients_bp, logger
from app.services import Session

@clients_bp.route('/photo/<int:id_client>', methods=['DELETE'])
def delete_client_photo(id_client: int):
    """Delete the (single) photo row for a given client id from tbl_photo_client.

    If multiple rows happen to exist (legacy), only the most recent (highest id_photo) is removed.
    Returns 404 if no row exists.
    """
    current_session = Session()
    try:
        result = current_session.execute(
            text("SELECT url_path FROM tbl_photo_client WHERE id_client = :id"),
            {"id": id_client}
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

        result = current_session.execute(
            text(
                """
                DELETE FROM tbl_photo_client
                WHERE id_client = :id_client
                RETURNING id_photo
                """
            ),
            {"id_client": id_client},
        )

        row = result.fetchone()
        
        if not row:
            current_session.rollback()
            return jsonify({"message": "No photo found for client", "id_client": id_client}), 404
        deleted_id = row._mapping['id_photo']
        current_session.commit()
        return jsonify({
            "message": "Client photo deleted successfully",
            "id_client": id_client,
            "id_photo_deleted": deleted_id
        }), 200
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error deleting client photo: {e}")
        return jsonify({"error": "Failed to delete client photo"}), 500
    finally:
        current_session.close()
