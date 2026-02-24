from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_lashing_condition(lashing_id, lashing_type):
    current_session = Session()
    print('get_dados_table_lifting')

    try:
        if lashing_type == "Shackles":
            query = """
                select 
                    tls.lashing_plan,
                    tls.lashing_items,
                    tls.lashing_material,
                    tls.lashing_condition,
                    tls.visible_mark,
                    tls.visible_grade_number,
                    tls.visible_limit,
                    tls.visible_pin_mark,
                    tls.visible_grade_material,
                    tls.compatible_pin,
                    tls.fractures,
                    tls.deformations,
                    tls.corrosion,
                    tls.wear,
                    tls.notches,
                    tls.overheating,
                    tls.bends,
                    tls.shackle_pin,
                    tls.tightened_pin,
                    tls.present_pin,
                    tls.lashing_shackles_acceptance
                from 
                tbl_lashing_shackles tls 
                where tls.id_lashing_material = :lifting_id
            """
        elif lashing_type == "Wire Ropes":
            query = """
                select 
                    tlw.lashing_plan,
                    tlw.lashing_items,
                    tlw.lashing_material,
                    tlw.lashing_condition,
                    tlw.broken_wires,
                    tlw.broken_wires_concentration,
                    tlw.broken_wires_terminal,
                    tlw.broken_wires_valley,
                    tlw.wear_wires_reduction,
                    tlw.wear_wires_localized,
                    tlw.wear_wires_uniform,
                    tlw.corrosion_wires_visible,
                    tlw.corrosion_wires_signs,
                    tlw.corrosion_wires_cavities,
                    tlw.deformation_wires_crushing,
                    tlw.deformation_wires_caging,
                    tlw.deformation_wires_protusion,
                    tlw.deformation_wires_knots,
                    tlw.deformation_wires_flattening,
                    tlw.other_wires_heat,
                    tlw.other_wires_electrical,
                    tlw.other_wires_strands,
                    tlw.other_wires_exposed,
                    tlw.other_wires_terminal,
                    tlw.lubrification_wires_lack,
                    tlw.lubrification_wires_drying,
                    tlw.conclusion_wires_suitable,
                    tlw.lashing_wires_acceptance
                from 
                tbl_lashing_wire tlw 
                where tlw.id_lashing_material = :id_lashing
            """
        elif lashing_type == "Tensioner, turnbuckle, arm lever":
            query = """
                select 
                    tlt.lashing_plan,
                    tlt.lashing_items,
                    tlt.lashing_material,
                    tlt.lashing_condition,
                    tlt.visible_mark,
                    tlt.legible_identification,
                    tlt.marked_limit,
                    tlt.visible_traceability,
                    tlt.cracks,
                    tlt.wear,
                    tlt.stretched,
                    tlt.twisted,
                    tlt.corrosion,
                    tlt.overheating,
                    tlt.lashing_tensioner_acceptance
                from 
                tbl_lashing_tensioner tlt
                where tlt.id_lashing_material = :id_lashing
            """
        elif lashing_type == "Stopper, dog plate":
            query = """
                select 
                    tls.lashing_plan,
                    tls.lashing_items,
                    tls.lashing_material,
                    tls.lashing_condition,
                    tls.dimensions,
                    tls.wear,
                    tls.twisted,
                    tls.corrosion,
                    tls.lashing_stopper_acceptance
                from 
                tbl_lashing_stopper tls
                where tls.id_lashing_material = :id_lashing
            """
        elif lashing_type == "Chain":
            query = """
                select 
                    tlc.lashing_plan,
                    tlc.lashing_items,
                    tlc.lashing_material,
                    tlc.lashing_condition,
                    tlc.visible_mark,
                    tlc.marked_grade,
                    tlc.marked_limit,
                    tlc.visible_traceability,
                    tlc.specified_length,
                    tlc.sling_number,
                    tlc.legible_identification,
                    tlc.marked_inspection,
                    tlc.links_cracks,
                    tlc.excessive_wear,
                    tlc.links_stretched,
                    tlc.links_twisted,
                    tlc.corrosion,
                    tlc.overheating,
                    tlc.weld_splatter,
                    tlc.links_obstructions,
                    tlc.links_diameter,
                    tlc.reduction_wear,
                    tlc.elongation_length,
                    tlc.lashing_chain_acceptance
                from 
                tbl_lashing_chain tlc 
                where tlc.id_lashing_material = :id_lashing
            """
        elif lashing_type == "Synthetic Lines":
            query = """
                select 
                    tls.lashing_plan,
                    tls.lashing_items,
                    tls.lashing_material,
                    tls.lashing_condition,
                    tls.missing_label,
                    tls.visible_capacity,
                    tls.core_exposure,
                    tls.core_cut,
                    tls.core_broken,
                    tls.core_abrasion,
                    tls.damages_protection,
                    tls.cut_any,
                    tls.cut_sides,
                    tls.punctures,
                    tls.abrasion,
                    tls.damages_heat,
                    tls.excessive_friction,
                    tls.knots,
                    tls.modifications,
                    tls.chemical_stains,
                    tls.overload,
                    tls.hardware_deformations,
                    tls.wear_metal,
                    tls.fractures,
                    tls.hook_deformations,
                    tls.lashing_lines_acceptance
                from 
                tbl_lashing_lines tls  
                where tls.id_lashing_material = :id_lashing
            """
        else:
            return None, f"Unsupported lashing_type: {lashing_type}"
        
        result = current_session.execute(
            text(query),
            {"id_lashing": lashing_id}
        ).mappings()

        rows = result.fetchall()

        if not rows:
            return None, f"Lashing ID {lashing_id} not found."

        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        if lashing_type == "Shackles":
            row = rows[0]
            data = {
                "lashing_plan": safe(row.get("lashing_plan")),
                "lashing_items": safe(row.get("lashing_items")),
                "lashing_material": safe(row.get("lashing_material")),
                "lashing_condition": safe(row.get("lashing_condition")),
                "visible_mark": safe(row.get("visible_mark")),
                "visible_grade_number": safe(row.get("visible_grade_number")),
                "visible_limit": safe(row.get("visible_limit")),
                "visible_pin_mark": safe(row.get("visible_pin_mark")),
                "visible_grade_material": safe(row.get("visible_grade_material")),
                "compatible_pin": safe(row.get("compatible_pin")),
                "fractures": safe(row.get("fractures")),
                "deformations": safe(row.get("deformations")),
                "corrosion": safe(row.get("corrosion")),
                "wear": safe(row.get("wear")),
                "notches": safe(row.get("notches")),
                "overheating": safe(row.get("overheating")),
                "bends": safe(row.get("bends")),
                "shackle_pin": safe(row.get("shackle_pin")),
                "tightened_pin": safe(row.get("tightened_pin")),
                "present_pin": safe(row.get("present_pin")),
                "lashing_shackles_acceptance": safe(row.get("lashing_shackles_acceptance"))
            }
        elif lashing_type == "Wire Ropes":
            row = rows[0]
            data = {
                "lashing_plan": safe(row.get("lashing_plan")),
                "lashing_items": safe(row.get("lashing_items")),
                "lashing_material": safe(row.get("lashing_material")),
                "lashing_condition": safe(row.get("lashing_condition")),
                "broken_wires": safe(row.get("broken_wires")),
                "broken_wires_concentration": safe(row.get("broken_wires_concentration")),
                "broken_wires_terminal": safe(row.get("broken_wires_terminal")),
                "broken_wires_valley": safe(row.get("broken_wires_valley")),
                "wear_wires_reduction": safe(row.get("wear_wires_reduction")),
                "wear_wires_localized": safe(row.get("wear_wires_localized")),
                "wear_wires_uniform": safe(row.get("wear_wires_uniform")),
                "corrosion_wires_visible": safe(row.get("corrosion_wires_visible")),
                "corrosion_wires_signs": safe(row.get("corrosion_wires_signs")),
                "corrosion_wires_cavities": safe(row.get("corrosion_wires_cavities")),
                "deformation_wires_crushing": safe(row.get("deformation_wires_crushing")),
                "deformation_wires_caging": safe(row.get("deformation_wires_caging")),
                "deformation_wires_protusion": safe(row.get("deformation_wires_protusion")),
                "deformation_wires_knots": safe(row.get("deformation_wires_knots")),
                "deformation_wires_flattening": safe(row.get("deformation_wires_flattening")),
                "other_wires_heat": safe(row.get("other_wires_heat")),
                "other_wires_electrical": safe(row.get("other_wires_electrical")),
                "other_wires_strands": safe(row.get("other_wires_strands")),
                "other_wires_exposed": safe(row.get("other_wires_exposed")),
                "other_wires_terminal": safe(row.get("other_wires_terminal")),
                "lubrification_wires_lack": safe(row.get("lubrification_wires_lack")),
                "lubrification_wires_drying": safe(row.get("lubrification_wires_drying")),
                "conclusion_wires_suitable": safe(row.get("conclusion_wires_suitable")),
                "lashing_wires_acceptance": safe(row.get("lashing_wires_acceptance"))
            }
        elif lashing_type == "Tensioner, turnbuckle, arm lever":
            row = rows[0]
            data = {
                "lashing_plan": safe(row.get("lashing_plan")),
                "lashing_items": safe(row.get("lashing_items")),
                "lashing_material": safe(row.get("lashing_material")),
                "lashing_condition": safe(row.get("lashing_condition")),
                "visible_mark": safe(row.get("visible_mark")),
                "legible_identification": safe(row.get("legible_identification")),
                "marked_limit": safe(row.get("marked_limit")),
                "visible_traceability": safe(row.get("visible_traceability")),
                "cracks": safe(row.get("cracks")),
                "wear": safe(row.get("wear")),
                "stretched": safe(row.get("stretched")),
                "twisted": safe(row.get("twisted")),
                "corrosion": safe(row.get("corrosion")),
                "overheating": safe(row.get("overheating")),
                "lashing_tensioner_acceptance": safe(row.get("lashing_tensioner_acceptance"))

            }
        elif lashing_type == "Stopper, dog plate":
            row = rows[0]
            data = {
                "lashing_plan": safe(row.get("lashing_plan")),
                "lashing_items": safe(row.get("lashing_items")),
                "lashing_material": safe(row.get("lashing_material")),
                "lashing_condition": safe(row.get("lashing_condition")),
                "dimensions": safe(row.get("dimensions")),
                "wear": safe(row.get("wear")),
                "twisted": safe(row.get("twisted")),
                "corrosion": safe(row.get("corrosion")),
                "lashing_stopper_acceptance": safe(row.get("lashing_stopper_acceptance"))
            }
        elif lashing_type == "Chain":
            row = rows[0]
            data = {
                "lashing_plan": safe(row.get("lashing_plan")),
                "lashing_items": safe(row.get("lashing_items")),
                "lashing_material": safe(row.get("lashing_material")),
                "lashing_condition": safe(row.get("lashing_condition")),
                "visible_mark": safe(row.get("visible_mark")),
                "marked_grade": safe(row.get("marked_grade")),
                "marked_limit": safe(row.get("marked_limit")),
                "visible_traceability": safe(row.get("visible_traceability")),
                "specified_length": safe(row.get("specified_length")),
                "sling_number": safe(row.get("sling_number")),
                "legible_identification": safe(row.get("legible_identification")),
                "marked_inspection": safe(row.get("marked_inspection")),
                "links_cracks": safe(row.get("links_cracks")),
                "excessive_wear": safe(row.get("excessive_wear")),
                "links_stretched": safe(row.get("links_stretched")),
                "links_twisted": safe(row.get("links_twisted")),
                "corrosion": safe(row.get("corrosion")),
                "overheating": safe(row.get("overheating")),
                "weld_splatter": safe(row.get("weld_splatter")),
                "links_obstructions": safe(row.get("links_obstructions")),
                "links_diameter": safe(row.get("links_diameter")),
                "reduction_wear": safe(row.get("reduction_wear")),
                "elongation_length": safe(row.get("elongation_length")),
                "lashing_chain_acceptance": safe(row.get("lashing_chain_acceptance"))
            }
        elif lashing_type == "Synthetic Lines":
            row = rows[0]
            data = {
                "lashing_plan": safe(row.get("lashing_plan")),
                "lashing_items": safe(row.get("lashing_items")),
                "lashing_material": safe(row.get("lashing_material")),
                "lashing_condition": safe(row.get("lashing_condition")),
                "missing_label": safe(row.get("missing_label")),
                "visible_capacity": safe(row.get("visible_capacity")),
                "core_exposure": safe(row.get("core_exposure")),
                "core_cut": safe(row.get("core_cut")),
                "core_broken": safe(row.get("core_broken")),
                "core_abrasion": safe(row.get("core_abrasion")),
                "damages_protection": safe(row.get("damages_protection")),
                "cut_any": safe(row.get("cut_any")),
                "cut_sides": safe(row.get("cut_sides")),
                "punctures": safe(row.get("punctures")),
                "abrasion": safe(row.get("abrasion")),
                "damages_heat": safe(row.get("damages_heat")),
                "excessive_friction": safe(row.get("excessive_friction")),
                "knots": safe(row.get("knots")),
                "modifications": safe(row.get("modifications")),
                "chemical_stains": safe(row.get("chemical_stains")),
                "overload": safe(row.get("overload")),
                "hardware_deformations": safe(row.get("hardware_deformations")),
                "wear_metal": safe(row.get("wear_metal")),
                "fractures": safe(row.get("fractures")),
                "hook_deformations": safe(row.get("hook_deformations")),
                "lashing_lines_acceptance": safe(row.get("lashing_lines_acceptance"))
            }
        else:
            return None, f"Unsupported lashing_type: {lashing_type}"

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on id_lashing {lashing_id}")
        return None, str(e)
    finally:
        current_session.close()