from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import relation_bp

@relation_bp.route('/<string:relation_type>/<int:id_rlt>', methods=['DELETE'])
def delete_relation(relation_type, id_rlt):
    """Delete relation by id"""
    current_session = Session()
    
    try:
        if relation_type == "Lashing":
            # Check if notification exists
            relation = current_session.execute(
                text("SELECT id_rlt FROM rlt_lashing_cargo WHERE id_rlt = :id"),
                {"id": id_rlt}
            )
            
            if not list(relation):
                return jsonify({"error": "Relation not found"}), 404
            
            current_session.execute(
                text("DELETE FROM rlt_lashing_cargo WHERE id_rlt = :id"),
                {"id": id_rlt}
            )
            
            current_session.commit()
            
            return jsonify({"message": "Relation deleted successfully"}), 200
        elif relation_type == "Lifting":
            # Check if notification exists
            relation = current_session.execute(
                text("SELECT id_rlt FROM rlt_lifting_cargo WHERE id_rlt = :id"),
                {"id": id_rlt}
            )
            
            if not list(relation):
                return jsonify({"error": "Relation not found"}), 404
            
            current_session.execute(
                text("DELETE FROM rlt_lifting_cargo WHERE id_rlt = :id"),
                {"id": id_rlt}
            )
            
            current_session.commit()
            
            return jsonify({"message": "Relation deleted successfully"}), 200
        else:
            return jsonify({"error": "Relation type not found"}), 404
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()