from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, lifting_inspection_bp
from .schema import (lifting_chain_schema, lifting_hook_schema, lifting_link_schema, lifting_shackles_schema,
                    lifting_sling_schema, lifting_wire_schema, lifting_spreader_schema
                    )

@lifting_inspection_bp.route('/<int:lifting_id>/<string:lifting_type>', methods=['PUT'])
def update_lifting_inspection(lifting_id, lifting_type):
    try:
        current_session = Session()

        try:
            if lifting_type == 'Wire Ropes':
                data = lifting_wire_schema.load(request.json, partial=True)
                # Verifica se o lifting existe
                lifting_exists = current_session.execute(
                    text("SELECT id_lifting_material FROM tbl_lifting_wire WHERE id_lifting_material = :id"),
                    {"id": lifting_id}
                )

                if not list(lifting_exists):
                    return jsonify({"error": "Lifting inspection not found"}), 404

                update_fields = []
                params = {"id": lifting_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "rigging_plan", "rigging_items", "rigging_material",
                    "rigging_condition", "broken_wires", "broken_wires_concentration",
                    "broken_wires_terminal", "broken_wires_valley", "wear_wires_reduction",
                    "wear_wires_localized", "wear_wires_uniform", "corrosion_wires_visible",
                    "corrosion_wires_signs", "corrosion_wires_cavities", "deformation_wires_crushing",
                    "deformation_wires_caging", "deformation_wires_protusion", "deformation_wires_knots",
                    "deformation_wires_flattening", "other_wires_heat", "other_wires_electrical",
                    "other_wires_strands", "other_wires_exposed", "other_wires_terminal",
                    "lubrification_wires_lack", "lubrification_wires_drying", "conclusion_wires_suitable",
                    "rigging_wires_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lifting_wire SET {', '.join(update_fields)} WHERE id_lifting_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lifting inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lifting_type == 'Synthetic Sling':
                data = lifting_sling_schema.load(request.json, partial=True)

                # Verifica se o lifting existe
                lifting_exists = current_session.execute(
                    text("SELECT id_lifting_material FROM tbl_lifting_sling WHERE id_lifting_material = :id"),
                    {"id": lifting_id}
                )

                if not list(lifting_exists):
                    return jsonify({"error": "Lifting inspection not found"}), 404

                update_fields = []
                params = {"id": lifting_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "rigging_plan", "rigging_items", "rigging_material",
                    "rigging_condition", "missing_label", "visible_capacity", "core_exposure",
                    "core_cut", "core_broken", "core_abrasion", "damages_protection", "cut_any",
                    "cut_sides", "punctures", "abrasion", "damages_heat", "excessive_friction",
                    "knots", "modifications", "chemical_stains", "overload", "hardware_deformations",
                    "wear_metal", "fractures", "hook_deformations", "rigging_sling_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lifting_sling SET {', '.join(update_fields)} WHERE id_lifting_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lifting inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lifting_type == 'Shackles':
                data = lifting_shackles_schema.load(request.json, partial=True)

                # Verifica se o lifting existe
                lifting_exists = current_session.execute(
                    text("SELECT id_lifting_material FROM tbl_lifting_shackles WHERE id_lifting_material = :id"),
                    {"id": lifting_id}
                )

                if not list(lifting_exists):
                    return jsonify({"error": "Lifting inspection not found"}), 404

                update_fields = []
                params = {"id": lifting_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "rigging_plan", "rigging_items", "rigging_material",
                    "rigging_condition", "visible_mark", "visible_grade_number", "visible_limit",
                    "visible_pin_mark", "visible_grade_material", "compatible_pin", "fractures",
                    "deformations", "corrosion", "wear", "notches", "overheating", "bends",
                    "shackle_pin", "tightened_pin", "present_pin", "rigging_shackles_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lifting_shackles SET {', '.join(update_fields)} WHERE id_lifting_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lifting inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lifting_type == 'Spreader':
                data = lifting_spreader_schema.load(request.json, partial=True)

                # Verifica se o lifting existe
                lifting_exists = current_session.execute(
                    text("SELECT id_lifting_material FROM tbl_lifting_spreader WHERE id_lifting_material = :id"),
                    {"id": lifting_id}
                )

                if not list(lifting_exists):
                    return jsonify({"error": "Lifting inspection not found"}), 404

                update_fields = []
                params = {"id": lifting_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "rigging_plan", "rigging_items", "rigging_material",
                    "rigging_condition", "marked_limit", "marked_weight", "main_fractures",
                    "permanent_deformations", "corrosion", "damages_collision", "twisting",
                    "overheating", "improper_repair", "contact_wear", "lifting_deformations",
                    "lifting_wear", "weld_fractures", "hole_deformations", "present_safety_devices",
                    "adjustment_mechanisms", "present_pin", "excessive_wear", "visible_mark",
                    "components_deformations", "locking_devices", "components_obstructions",
                    "rigging_spreader_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lifting_spreader SET {', '.join(update_fields)} WHERE id_lifting_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lifting inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lifting_type == 'Chain':
                data = lifting_chain_schema.load(request.json, partial=True)
                # Verifica se o lifting existe
                lifting_exists = current_session.execute(
                    text("SELECT id_lifting_material FROM tbl_lifting_chain WHERE id_lifting_material = :id"),
                    {"id": lifting_id}
                )

                if not list(lifting_exists):
                    return jsonify({"error": "Lifting inspection not found"}), 404

                update_fields = []
                params = {"id": lifting_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "rigging_plan", "rigging_items", "rigging_material",
                    "rigging_condition", "visible_mark", "marked_grade", "marked_limit",
                    "visible_traceability", "specified_length", "sling_number", "legible_identification",
                    "marked_inspection", "links_cracks", "excessive_wear", "links_stretched",
                    "links_twisted", "corrosion", "overheating", "weld_splatter", "links_obstructions",
                    "links_diameter", "reduction_wear", "elongation_length", "rigging_chain_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lifting_chain SET {', '.join(update_fields)} WHERE id_lifting_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lifting inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lifting_type == 'Hook':
                data = lifting_hook_schema.load(request.json, partial=True)

                # Verifica se o lifting existe
                lifting_exists = current_session.execute(
                    text("SELECT id_lifting_material FROM tbl_lifting_hook WHERE id_lifting_material = :id"),
                    {"id": lifting_id}
                )

                if not list(lifting_exists):
                    return jsonify({"error": "Lifting inspection not found"}), 404

                update_fields = []
                params = {"id": lifting_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "rigging_plan", "rigging_items", "rigging_material",
                    "rigging_condition", "visible_mark", "marked_limit", "visible_traceability", 
                    "hook_type", "marked_grade", "legible_identification", "cracks", "dents",
                    "excessive_corrosion", "visible_deformations", "overheating", "weld_splatter",
                    "unauthorized_modifications", "damages_thread", "throat_limits", "opening_deformations",
                    "excessive_wear_area", "sharp_edges", "widening_tip", "bearing_wear",
                    "impact_mark", "hook_shape", "intact_latch", "correctly_latch", "tension_latch",
                    "deformations_latch", "exessive_wear_points", "opening_latch", "corrosion_latch",
                    "damages_latch", "hook_rotation", "locking_mechanism", "smooth_joints", "jamming",
                    "automatic_latch", "excessive_play", "hook_dimensions", "reduction_wear",
                    "throat_opening", "elongation", "angular_deformations", "rigging_hook_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lifting_hook SET {', '.join(update_fields)} WHERE id_lifting_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lifting inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif lifting_type == 'Master Link':
                data = lifting_link_schema.load(request.json, partial=True)
                # Verifica se o lifting existe
                lifting_exists = current_session.execute(
                    text("SELECT id_lifting_material FROM tbl_lifting_link WHERE id_lifting_material = :id"),
                    {"id": lifting_id}
                )

                if not list(lifting_exists):
                    return jsonify({"error": "Lifting inspection not found"}), 404

                update_fields = []
                params = {"id": lifting_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "rigging_plan", "rigging_items", "rigging_material",
                    "rigging_condition", "visible_mark", "marked_limit", "marked_dimension",
                    "marked_grade", "visible_traceability", "cracks", "wear", "corrosion",
                    "visible_deformations", "overheating", "weld_splatter", "modifications",
                    "stretching", "original_shape", "contact_deformations", "sharp_edges", "impact_mark",
                    "section_reduction", "deep_scratches", "tolerated_dimensions", "reduction_wear",
                    "elongation", "angular_deformations", "rigging_link_acceptance"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_lifting_link SET {', '.join(update_fields)} WHERE id_lifting_material = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Lifting inspection updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            else:
                return jsonify({"error": "Lifting type found"}), 404
        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating lifting inspection: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400