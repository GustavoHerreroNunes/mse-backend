from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_lifting_condition(lifting_id, lifting_type):
    current_session = Session()
    print('get_dados_table_lifting')

    try:
        if lifting_type == "Shackles":
            query = """
                select 
                    tls.rigging_plan,
                    tls.rigging_items,
                    tls.rigging_material,
                    tls.rigging_condition,
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
                    tls.rigging_shackles_acceptance
                from 
                tbl_lifting_shackles tls 
                where tls.id_lifting_material = :lifting_id
            """
        elif lifting_type == "Wire Ropes":
            query = """
                select 
                    tlw.rigging_plan,
                    tlw.rigging_items,
                    tlw.rigging_material,
                    tlw.rigging_condition,
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
                    tlw.rigging_wires_acceptance
                from 
                tbl_lifting_wire tlw 
                where tlw.id_lifting_material = :lifting_id
            """
        elif lifting_type == "Hook":
            query = """
                select 
                    tlh.rigging_plan,
                    tlh.rigging_items,
                    tlh.rigging_material,
                    tlh.rigging_condition,
                    tlh.visible_mark,
                    tlh.marked_limit,
                    tlh.visible_traceability,
                    tlh.hook_type,
                    tlh.marked_grade,
                    tlh.legible_identification,
                    tlh.cracks,
                    tlh.dents,
                    tlh.excessive_corrosion,
                    tlh.visible_deformations,
                    tlh.overheating,
                    tlh.weld_splatter,
                    tlh.unauthorized_modifications,
                    tlh.damages_thread,
                    tlh.throat_limits,
                    tlh.opening_deformations,
                    tlh.excessive_wear_area,
                    tlh.sharp_edges,
                    tlh.widening_tip,
                    tlh.bearing_wear,
                    tlh.impact_mark,
                    tlh.hook_shape,
                    tlh.intact_latch,
                    tlh.correctly_latch,
                    tlh.tension_latch,
                    tlh.deformations_latch,
                    tlh.exessive_wear_points,
                    tlh.opening_latch,
                    tlh.corrosion_latch,
                    tlh.damages_latch,
                    tlh.hook_rotation,
                    tlh.locking_mechanism,
                    tlh.smooth_joints,
                    tlh.jamming,
                    tlh.automatic_latch,
                    tlh.excessive_play,
                    tlh.hook_dimensions,
                    tlh.reduction_wear,
                    tlh.throat_opening,
                    tlh.elongation,
                    tlh.angular_deformations,
                    tlh.rigging_hook_acceptance
                from 
                tbl_lifting_hook tlh 
                where tlh.id_lifting_material = :lifting_id
            """
        elif lifting_type == "Master Link":
            query = """
                select 
                    tll.rigging_plan,
                    tll.rigging_items,
                    tll.rigging_material,
                    tll.rigging_condition,
                    tll.visible_mark,
                    tll.marked_limit,
                    tll.marked_dimension,
                    tll.marked_grade,
                    tll.visible_traceability,
                    tll.cracks,
                    tll.wear,
                    tll.corrosion,
                    tll.visible_deformations,
                    tll.overheating,
                    tll.weld_splatter,
                    tll.modifications,
                    tll.stretching,
                    tll.original_shape,
                    tll.contact_deformations,
                    tll.sharp_edges,
                    tll.impact_mark,
                    tll.section_reduction,
                    tll.deep_scratches,
                    tll.tolerated_dimensions,
                    tll.reduction_wear,
                    tll.elongation,
                    tll.angular_deformations,
                    tll.rigging_link_acceptance
                from 
                tbl_lifting_link tll  
                where tll.id_lifting_material = :lifting_id
            """
        elif lifting_type == "Chain":
            query = """
                select 
                    tlc.rigging_plan,
                    tlc.rigging_items,
                    tlc.rigging_material,
                    tlc.rigging_condition,
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
                    tlc.rigging_chain_acceptance
                from 
                tbl_lifting_chain tlc 
                where tlc.id_lifting_material = :lifting_id
            """
        elif lifting_type == "Spreader":
            query = """
                select 
                    tls.rigging_plan,
                    tls.rigging_items,
                    tls.rigging_material,
                    tls.rigging_condition,
                    tls.marked_limit,
                    tls.marked_weight,
                    tls.main_fractures,
                    tls.permanent_deformations,
                    tls.corrosion,
                    tls.damages_collision,
                    tls.twisting,
                    tls.overheating,
                    tls.improper_repair,
                    tls.contact_wear,
                    tls.lifting_deformations,
                    tls.lifting_wear,
                    tls.weld_fractures,
                    tls.hole_deformations,
                    tls.present_safety_devices,
                    tls.adjustment_mechanisms,
                    tls.present_pin,
                    tls.excessive_wear,
                    tls.visible_mark,
                    tls.components_deformations,
                    tls.locking_devices,
                    tls.components_obstructions,
                    tls.rigging_spreader_acceptance
                from 
                tbl_lifting_spreader tls 
                where tls.id_lifting_material = :lifting_id
            """
        elif lifting_type == "Synthetic Sling":
            query = """
                select 
                    tls.rigging_plan,
                    tls.rigging_items,
                    tls.rigging_material,
                    tls.rigging_condition,
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
                    tls.rigging_sling_acceptance
                from 
                tbl_lifting_sling tls  
                where tls.id_lifting_material = :lifting_id
            """
        else:
            return None, f"Unsupported lifting_type: {lifting_type}"
        
        result = current_session.execute(
            text(query),
            {"lifting_id": lifting_id}
        ).mappings()

        rows = result.fetchall()

        if not rows:
            return None, f"Lifting ID {lifting_id} not found."

        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        if lifting_type == "Shackles":
            row = rows[0]
            data = {
                "rigging_plan": safe(row.get("rigging_plan")),
                "rigging_items": safe(row.get("rigging_items")),
                "rigging_material": safe(row.get("rigging_material")),
                "rigging_condition": safe(row.get("rigging_condition")),
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
                "rigging_shackles_acceptance": safe(row.get("rigging_shackles_acceptance"))
            }
        elif lifting_type == "Wire Ropes":
            row = rows[0]
            data = {
                "rigging_plan": safe(row.get("rigging_plan")),
                "rigging_items": safe(row.get("rigging_items")),
                "rigging_material": safe(row.get("rigging_material")),
                "rigging_condition": safe(row.get("rigging_condition")),
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
                "rigging_wires_acceptance": safe(row.get("rigging_wires_acceptance"))
            }
        elif lifting_type == "Hook":
            row = rows[0]
            data = {
                "rigging_plan": safe(row.get("rigging_plan")),
                "rigging_items": safe(row.get("rigging_items")),
                "rigging_material": safe(row.get("rigging_material")),
                "rigging_condition": safe(row.get("rigging_condition")),
                "visible_mark": safe(row.get("visible_mark")),
                "marked_limit": safe(row.get("marked_limit")),
                "visible_traceability": safe(row.get("visible_traceability")),
                "hook_type": safe(row.get("hook_type")),
                "marked_grade": safe(row.get("marked_grade")),
                "legible_identification": safe(row.get("legible_identification")),
                "cracks": safe(row.get("cracks")),
                "dents": safe(row.get("dents")),
                "excessive_corrosion": safe(row.get("excessive_corrosion")),
                "visible_deformations": safe(row.get("visible_deformations")),
                "overheating": safe(row.get("overheating")),
                "weld_splatter": safe(row.get("weld_splatter")),
                "unauthorized_modifications": safe(row.get("unauthorized_modifications")),
                "damages_thread": safe(row.get("damages_thread")),
                "throat_limits": safe(row.get("throat_limits")),
                "opening_deformations": safe(row.get("opening_deformations")),
                "excessive_wear_area": safe(row.get("excessive_wear_area")),
                "sharp_edges": safe(row.get("sharp_edges")),
                "widening_tip": safe(row.get("widening_tip")),
                "bearing_wear": safe(row.get("bearing_wear")),
                "impact_mark": safe(row.get("impact_mark")),
                "hook_shape": safe(row.get("hook_shape")),
                "intact_latch": safe(row.get("intact_latch")),
                "correctly_latch": safe(row.get("correctly_latch")),
                "tension_latch": safe(row.get("tension_latch")),
                "deformations_latch": safe(row.get("deformations_latch")),
                "exessive_wear_points": safe(row.get("exessive_wear_points")),
                "opening_latch": safe(row.get("opening_latch")),
                "corrosion_latch": safe(row.get("corrosion_latch")),
                "damages_latch": safe(row.get("damages_latch")),
                "hook_rotation": safe(row.get("hook_rotation")),
                "locking_mechanism": safe(row.get("locking_mechanism")),
                "smooth_joints": safe(row.get("smooth_joints")),
                "jamming": safe(row.get("jamming")),
                "automatic_latch": safe(row.get("automatic_latch")),
                "excessive_play": safe(row.get("excessive_play")),
                "hook_dimensions": safe(row.get("hook_dimensions")),
                "reduction_wear": safe(row.get("reduction_wear")),
                "throat_opening": safe(row.get("throat_opening")),
                "elongation": safe(row.get("elongation")),
                "angular_deformations": safe(row.get("angular_deformations")),
                "rigging_hook_acceptance": safe(row.get("rigging_hook_acceptance"))
            }
        elif lifting_type == "Master Link":
            row = rows[0]
            data = {
                "rigging_plan": safe(row.get("rigging_plan")),
                "rigging_items": safe(row.get("rigging_items")),
                "rigging_material": safe(row.get("rigging_material")),
                "rigging_condition": safe(row.get("rigging_condition")),
                "visible_mark": safe(row.get("visible_mark")),
                "marked_limit": safe(row.get("marked_limit")),
                "marked_dimension": safe(row.get("marked_dimension")),
                "marked_grade": safe(row.get("marked_grade")),
                "visible_traceability": safe(row.get("visible_traceability")),
                "cracks": safe(row.get("cracks")),
                "wear": safe(row.get("wear")),
                "corrosion": safe(row.get("corrosion")),
                "visible_deformations": safe(row.get("visible_deformations")),
                "overheating": safe(row.get("overheating")),
                "weld_splatter": safe(row.get("weld_splatter")),
                "modifications": safe(row.get("modifications")),
                "stretching": safe(row.get("stretching")),
                "original_shape": safe(row.get("original_shape")),
                "contact_deformations": safe(row.get("contact_deformations")),
                "sharp_edges": safe(row.get("sharp_edges")),
                "impact_mark": safe(row.get("impact_mark")),
                "section_reduction": safe(row.get("section_reduction")),
                "deep_scratches": safe(row.get("deep_scratches")),
                "tolerated_dimensions": safe(row.get("tolerated_dimensions")),
                "reduction_wear": safe(row.get("reduction_wear")),
                "elongation": safe(row.get("elongation")),
                "angular_deformations": safe(row.get("angular_deformations")),
                "rigging_link_acceptance": safe(row.get("rigging_link_acceptance"))
            }
        elif lifting_type == "Chain":
            row = rows[0]
            data = {
                "rigging_plan": safe(row.get("rigging_plan")),
                "rigging_items": safe(row.get("rigging_items")),
                "rigging_material": safe(row.get("rigging_material")),
                "rigging_condition": safe(row.get("rigging_condition")),
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
                "rigging_chain_acceptance": safe(row.get("rigging_chain_acceptance"))
            }
        elif lifting_type == "Spreader":
            row = rows[0]
            data = {
                "rigging_plan": safe(row.get("rigging_plan")),
                "rigging_items": safe(row.get("rigging_items")),
                "rigging_material": safe(row.get("rigging_material")),
                "rigging_condition": safe(row.get("rigging_condition")),
                "marked_limit": safe(row.get("marked_limit")),
                "marked_weight": safe(row.get("marked_weight")),
                "main_fractures": safe(row.get("main_fractures")),
                "permanent_deformations": safe(row.get("permanent_deformations")),
                "corrosion": safe(row.get("corrosion")),
                "damages_collision": safe(row.get("damages_collision")),
                "twisting": safe(row.get("twisting")),
                "overheating": safe(row.get("overheating")),
                "improper_repair": safe(row.get("improper_repair")),
                "contact_wear": safe(row.get("contact_wear")),
                "lifting_deformations": safe(row.get("lifting_deformations")),
                "lifting_wear": safe(row.get("lifting_wear")),
                "weld_fractures": safe(row.get("weld_fractures")),
                "hole_deformations": safe(row.get("hole_deformations")),
                "present_safety_devices": safe(row.get("present_safety_devices")),
                "adjustment_mechanisms": safe(row.get("adjustment_mechanisms")),
                "present_pin": safe(row.get("present_pin")),
                "excessive_wear": safe(row.get("excessive_wear")),
                "visible_mark": safe(row.get("visible_mark")),
                "components_deformations": safe(row.get("components_deformations")),
                "locking_devices": safe(row.get("locking_devices")),
                "components_obstructions": safe(row.get("components_obstructions")),
                "rigging_spreader_acceptance": safe(row.get("rigging_spreader_acceptance"))
            }
        elif lifting_type == "Synthetic Sling":
            row = rows[0]
            data = {
                "rigging_plan": safe(row.get("rigging_plan")),
                "rigging_items": safe(row.get("rigging_items")),
                "rigging_material": safe(row.get("rigging_material")),
                "rigging_condition": safe(row.get("rigging_condition")),
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
                "rigging_sling_acceptance": safe(row.get("rigging_sling_acceptance"))
            }
        else:
            return None, f"Unsupported lifting_type: {lifting_type}"

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on lifting_id {lifting_id}")
        return None, str(e)
    finally:
        current_session.close()