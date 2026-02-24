from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, lashing_inspection_bp
from .schema import (lashing_chain_schema, lashing_shackles_schema, lashing_lines_schema, 
                     lashing_wire_schema, lashing_stopper_schema, lashing_tensioner_schema
                    )

@lashing_inspection_bp.route('/<int:lashing_id>/<string:lashing_type>', methods=['PUT'])
def update_lashing_inspection(lashing_id, lashing_type):
    try:
        current_session = Session()

        try:
            if lashing_type == 'Wire Ropes':
                data = lashing_wire_schema.load(request.json, partial=True)
                # Verifica se o lashing existe
                lashing_exists = current_session.execute(
                    text("SELECT id_lashing_material FROM tbl_lashing_wire WHERE id_lashing_material = :id"),
                    {"id": lashing_id}
                )

                if not list(lashing_exists):
                    return jsonify({"error": "Lashing inspection not found"}), 404

                update_fields = []
                params = {"id": lashing_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "lashing_plan", "lashing_items", "lashing_material",
                    "lashing_condition", "broken_wires", "broken_wires_concentration",
                    "broken_wires_terminal", "broken_wires_valley", "wear_wires_reduction",
                    "wear_wires_localized", "wear_wires_uniform", "corrosion_wires_visible",
                    "corrosion_wires_signs", "corrosion_wires_cavities", "deformation_wires_crushing",
                    "deformation_wires_caging", "deformation_wires_protusion", "deformation_wires_knots",
                    "deformation_wires_flattening", "other_wires_heat", "other_wires_electrical",
                    "other_wires_strands", "other_wires_exposed", "other_wires_terminal",
                    "lubrification_wires_lack", "lubrification_wires_drying", "conclusion_wires_suitable",
                    "lashing_wires_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lashing_wire SET {', '.join(update_fields)} WHERE id_lashing_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lashing inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lashing_type == 'Synthetic Lines':
                data = lashing_lines_schema.load(request.json, partial=True)

                # Verifica se o lashing existe
                lashing_exists = current_session.execute(
                    text("SELECT id_lashing_material FROM tbl_lashing_lines WHERE id_lashing_material = :id"),
                    {"id": lashing_id}
                )

                if not list(lashing_exists):
                    return jsonify({"error": "Lashing inspection not found"}), 404

                update_fields = []
                params = {"id": lashing_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "lashing_plan", "lashing_items", "lashing_material",
                    "lashing_condition", "missing_label", "visible_capacity", "core_exposure",
                    "core_cut", "core_broken", "core_abrasion", "damages_protection", "cut_any",
                    "cut_sides", "punctures", "abrasion", "damages_heat", "excessive_friction",
                    "knots", "modifications", "chemical_stains", "overload", "hardware_deformations",
                    "wear_metal", "fractures", "hook_deformations", "lashing_lines_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lashing_lines SET {', '.join(update_fields)} WHERE id_lashing_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lashing inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lashing_type == 'Shackles':
                data = lashing_shackles_schema.load(request.json, partial=True)

                # Verifica se o lashing existe
                lashing_exists = current_session.execute(
                    text("SELECT id_lashing_material FROM tbl_lashing_shackles WHERE id_lashing_material = :id"),
                    {"id": lashing_id}
                )

                if not list(lashing_exists):
                    return jsonify({"error": "Lashing inspection not found"}), 404

                update_fields = []
                params = {"id": lashing_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "lashing_plan", "lashing_items", "lashing_material",
                    "lashing_condition", "visible_mark", "visible_grade_number", "visible_limit",
                    "visible_pin_mark", "visible_grade_material", "compatible_pin", "fractures",
                    "deformations", "corrosion", "wear", "notches", "overheating", "bends",
                    "shackle_pin", "tightened_pin", "present_pin", "lashing_shackles_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lashing_shackles SET {', '.join(update_fields)} WHERE id_lashing_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lashing inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lashing_type == 'Chain':
                data = lashing_chain_schema.load(request.json, partial=True)
                # Verifica se o lashing existe
                lashing_exists = current_session.execute(
                    text("SELECT id_lashing_material FROM tbl_lashing_chain WHERE id_lashing_material = :id"),
                    {"id": lashing_id}
                )

                if not list(lashing_exists):
                    return jsonify({"error": "Lashing inspection not found"}), 404

                update_fields = []
                params = {"id": lashing_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "lashing_plan", "lashing_items", "lashing_material",
                    "lashing_condition", "visible_mark", "marked_grade", "marked_limit",
                    "visible_traceability", "specified_length", "sling_number", "legible_identification",
                    "marked_inspection", "links_cracks", "excessive_wear", "links_stretched",
                    "links_twisted", "corrosion", "overheating", "weld_splatter", "links_obstructions",
                    "links_diameter", "reduction_wear", "elongation_length", "lashing_chain_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lashing_chain SET {', '.join(update_fields)} WHERE id_lashing_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lashing inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lashing_type == 'Stopper, dog plate':
                data = lashing_stopper_schema.load(request.json, partial=True)

                # Verifica se o lashing existe
                lashing_exists = current_session.execute(
                    text("SELECT id_lashing_material FROM tbl_lashing_stopper WHERE id_lashing_material = :id"),
                    {"id": lashing_id}
                )

                if not list(lashing_exists):
                    return jsonify({"error": "Lashing inspection not found"}), 404

                update_fields = []
                params = {"id": lashing_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "lashing_plan", "lashing_items", "lashing_material",
                    "lashing_condition", "dimensions", "wear", "twisted", "corrosion", 
                    "lashing_stopper_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lashing_stopper SET {', '.join(update_fields)} WHERE id_lashing_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lashing inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lashing_type == 'Tensioner, turnbuckle, arm lever':
                data = lashing_tensioner_schema.load(request.json, partial=True)
                # Verifica se o lashing existe
                lashing_exists = current_session.execute(
                    text("SELECT id_lashing_material FROM tbl_lashing_tensioner WHERE id_lashing_material = :id"),
                    {"id": lashing_id}
                )

                if not list(lashing_exists):
                    return jsonify({"error": "Lashing inspection not found"}), 404

                update_fields = []
                params = {"id": lashing_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "lashing_plan", "lashing_items", "lashing_material",
                    "lashing_condition", "visible_mark", "legible_identification", "marked_limit",
                    "visible_traceability", "cracks", "wear", "stretched", "twisted", "corrosion",
                    "overheating", "lashing_tensioner_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lashing_tensioner SET {', '.join(update_fields)} WHERE id_lashing_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lashing inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            else:
                return jsonify({"error": "Lashing type found"}), 404
        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating lashing inspection: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400