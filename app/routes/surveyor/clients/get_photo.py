from flask import jsonify
from sqlalchemy import text

from . import clients_bp, logger
from app.services import Session
from .schema import photo_client_list_schema

@clients_bp.route('/photo/<int:id_client>', methods=['GET'])
def get_client_photo(id_client: int):
    """Retrieve the latest photo record for a client from tbl_photo_client.

    Returns 404 if no photo exists for the given client.
    """
    session = Session()
    try:
        result = session.execute(
            text(
                """
                SELECT id_photo, id_client, url_path
                FROM tbl_photo_client
                WHERE id_client = :id_client
                ORDER BY id_photo DESC
                """
            ),
            {"id_client": id_client},
        )

        return photo_client_list_schema.dump(result)
    except Exception as e:
        logger.error(f"Error retrieving client photo: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
