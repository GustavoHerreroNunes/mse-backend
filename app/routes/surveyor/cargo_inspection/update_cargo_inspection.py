from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, cargo_inspection_bp
from .schema import (cargo_wood_schema, cargo_bale_schema, cargo_machinery_schema, cargo_metallic_schema,
                    cargo_reel_schema, cargo_steel_schema, cargo_thd_schema
                    )

@cargo_inspection_bp.route('/<int:cargo_id>/<string:cargo_type>', methods=['PUT'])
def update_cargo_inspection(cargo_id, cargo_type):
    try:
        current_session = Session()

        try:
            if cargo_type == 'Wooden Crate':
                data = cargo_wood_schema.load(request.json, partial=True)
                # Verifica se o cargo existe
                cargo_exists = current_session.execute(
                    text("SELECT cargo_id FROM tbl_cargo_condition_wood WHERE cargo_id = :id"),
                    {"id": cargo_id}
                )

                if not list(cargo_exists):
                    return jsonify({"error": "Cargo condition not found"}), 404

                update_fields = []
                params = {"id": cargo_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "breakage",
                    "ranking_breakage",
                    "moisture",
                    "ranking_moisture",
                    "infestation",
                    "ranking_infestation"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_cargo_condition_wood SET {', '.join(update_fields)} WHERE cargo_id = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Cargo condition updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif cargo_type == 'Steel Pipes':
                data = cargo_steel_schema.load(request.json, partial=True)

                # Verifica se o cargo existe
                cargo_exists = current_session.execute(
                    text("SELECT cargo_id FROM tbl_cargo_condition_steel WHERE cargo_id = :id"),
                    {"id": cargo_id}
                )

                if not list(cargo_exists):
                    return jsonify({"error": "Cargo condition not found"}), 404

                update_fields = []
                params = {"id": cargo_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "denting", "ranking_denting", "ovality", "ranking_ovality",
                    "corrosion", "ranking_corrosion", "damages_end", "ranking_damages_end",
                    "damages_coating", "ranking_damages_coating", "scratches", "ranking_scratches",
                    "endcaps", "ranking_endcaps"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_cargo_condition_steel SET {', '.join(update_fields)} WHERE cargo_id = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Cargo condition updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif cargo_type == 'Machinery':
                data = cargo_machinery_schema.load(request.json, partial=True)

                # Verifica se o cargo existe
                cargo_exists = current_session.execute(
                    text("SELECT cargo_id FROM tbl_cargo_condition_machinery WHERE cargo_id = :id"),
                    {"id": cargo_id}
                )

                if not list(cargo_exists):
                    return jsonify({"error": "Cargo condition not found"}), 404

                update_fields = []
                params = {"id": cargo_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "damages_mechanical", "ranking_damages_mechanical", "broken_wires",
                    "ranking_broken_wires", "leaks", "ranking_leaks", "corrosion",
                    "ranking_corrosion", "broken_hydraulic", "ranking_broken_hydraulic",
                    "broken_control", "ranking_broken_control", "broken_gauges",
                    "ranking_broken_gauges", "scratches", "ranking_scratches"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_cargo_condition_machinery SET {', '.join(update_fields)} WHERE cargo_id = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Cargo condition updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif cargo_type == 'Xtree or THD':
                data = cargo_thd_schema.load(request.json, partial=True)

                # Verifica se o cargo existe
                cargo_exists = current_session.execute(
                    text("SELECT cargo_id FROM tbl_cargo_condition_thd WHERE cargo_id = :id"),
                    {"id": cargo_id}
                )

                if not list(cargo_exists):
                    return jsonify({"error": "Cargo condition not found"}), 404

                update_fields = []
                params = {"id": cargo_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "damages_mechanical", "ranking_damages_mechanical", "broken_wires",
                    "ranking_broken_wires", "leaks", "ranking_leaks", "corrosion", "ranking_corrosion",
                    "broken_hydraulic", "ranking_broken_hydraulic", "broken_control", "ranking_broken_control",
                    "broken_gauges", "ranking_broken_gauges", "coating", "ranking_coating",
                    "broken_anodes", "ranking_broken_anodes", "tarphauling", "ranking_tarphauling",
                    "broken_lashing", "ranking_broken_lashing", "elements_order", "ranking_elements_order"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_cargo_condition_thd SET {', '.join(update_fields)} WHERE cargo_id = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Cargo condition updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif cargo_type == 'Bale or Bagged':
                data = cargo_bale_schema.load(request.json, partial=True)
                # Verifica se o cargo existe
                cargo_exists = current_session.execute(
                    text("SELECT cargo_id FROM tbl_cargo_condition_bale WHERE cargo_id = :id"),
                    {"id": cargo_id}
                )

                if not list(cargo_exists):
                    return jsonify({"error": "Cargo condition not found"}), 404

                update_fields = []
                params = {"id": cargo_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "tears", "ranking_tears", "moisture",
                    "ranking_moisture", "contamination", "ranking_contamination",
                    "deformation", "ranking_deformation", "strapping",
                    "ranking_strapping", "expected_cargo", "ranking_expected_cargo"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_cargo_condition_bale SET {', '.join(update_fields)} WHERE cargo_id = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Cargo condition updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif cargo_type == 'Metallic':
                data = cargo_metallic_schema.load(request.json, partial=True)

                # Verifica se o cargo existe
                cargo_exists = current_session.execute(
                    text("SELECT cargo_id FROM tbl_cargo_condition_metallic WHERE cargo_id = :id"),
                    {"id": cargo_id}
                )

                if not list(cargo_exists):
                    return jsonify({"error": "Cargo condition not found"}), 404

                update_fields = []
                params = {"id": cargo_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "corrosion", "ranking_corrosion", "deformation",
                    "ranking_deformation", "scratches", "ranking_scratches",
                    "damages_weld", "ranking_damages_weld", "pitting_marks",
                    "ranking_pitting_marks", "chemical_traces", "ranking_chemical_traces",
                    "heat_marks", "ranking_heat_marks"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_cargo_condition_metallic SET {', '.join(update_fields)} WHERE cargo_id = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Cargo condition updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            elif cargo_type == 'Reel':
                data = cargo_reel_schema.load(request.json, partial=True)
                # Verifica se o cargo existe
                cargo_exists = current_session.execute(
                    text("SELECT cargo_id FROM tbl_cargo_condition_reel WHERE cargo_id = :id"),
                    {"id": cargo_id}
                )

                if not list(cargo_exists):
                    return jsonify({"error": "Cargo condition not found"}), 404

                update_fields = []
                params = {"id": cargo_id}

                # Campos que podem ser atualizados
                fields_to_update = [
                    "corrosion", "ranking_corrosion", "deformation_berth",
                    "ranking_deformation_berth", "deformation_lifting", "ranking_deformation_lifting",
                    "deformation_lashing", "ranking_deformation_lashing", "tears",
                    "ranking_tears", "heat_marks", "ranking_heat_marks", "damages_weld",
                    "ranking_damages_weld", "scratches", "ranking_scratches", "pitting_marks",
                    "ranking_pitting_marks", "damages_pipe", "ranking_damages_pipe"
                ]

                for field in fields_to_update:
                    if field in data:
                        update_fields.append(f"{field} = :{field}")
                        params[field] = data[field]

                if update_fields:
                    query = f"UPDATE tbl_cargo_condition_reel SET {', '.join(update_fields)} WHERE cargo_id = :id"
                    current_session.execute(text(query), params)
                    current_session.commit()

                    return jsonify({"message": "Cargo condition updated successfully"}), 200
                else:
                    return jsonify({"message": "No fields provided for update"}), 400
            else:
                return jsonify({"error": "Cargo type not found"}), 404
        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating cargo condition: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400