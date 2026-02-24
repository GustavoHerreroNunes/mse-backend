from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_ia_conclusion_lifting(demanda_id):
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            SELECT 
                CASE 
                    WHEN COUNT(*) > 0 AND 
                        SUM(
                            CASE 
                                WHEN 
                                    tlm.type = 'Chain' and
                                    tlc.rigging_plan IN ('Yes', 'Does not apply') AND
                                    tlc.rigging_items IN ('Yes', 'Does not apply') AND
                                    tlc.rigging_material IN ('Yes', 'Does not apply') AND
                                    tlc.rigging_condition IN ('Yes', 'Does not apply') AND
                                    tlc.visible_mark IN ('Yes', 'Does not apply') AND
                                    tlc.marked_grade IN ('Yes', 'Does not apply') AND
                                    tlc.marked_limit IN ('Yes', 'Does not apply') AND
                                    tlc.visible_traceability IN ('Yes', 'Does not apply') AND
                                    tlc.specified_length IN ('Yes', 'Does not apply') AND
                                    tlc.sling_number IN ('Yes', 'Does not apply') AND
                                    tlc.legible_identification IN ('Yes', 'Does not apply') AND
                                    tlc.marked_inspection IN ('Yes', 'Does not apply') AND
                                    tlc.links_cracks IN ('Yes', 'Does not apply') AND
                                    tlc.excessive_wear IN ('Yes', 'Does not apply') AND
                                    tlc.links_stretched IN ('Yes', 'Does not apply') AND
                                    tlc.links_twisted IN ('Yes', 'Does not apply') AND
                                    tlc.corrosion IN ('Yes', 'Does not apply') AND
                                    tlc.overheating IN ('Yes', 'Does not apply') AND
                                    tlc.weld_splatter IN ('Yes', 'Does not apply') AND
                                    tlc.links_obstructions IN ('Yes', 'Does not apply') AND
                                    tlc.links_diameter IN ('Yes', 'Does not apply') AND
                                    tlc.reduction_wear IN ('No', 'Does not apply') AND
                                    tlc.elongation_length IN ('No', 'Does not apply') AND
                                    tlc.rigging_chain_acceptance IN ('Yes', 'Does not apply')
                                THEN 1 
                                WHEN 
                                    tlm.type = 'Hook' and
                                    tlh.rigging_plan IN ('Yes', 'Does not apply') AND
                                    tlh.rigging_items IN ('Yes', 'Does not apply') AND
                                    tlh.rigging_material IN ('Yes', 'Does not apply') AND
                                    tlh.rigging_condition IN ('Yes', 'Does not apply') AND
                                    tlh.visible_mark IN ('Yes', 'Does not apply') AND
                                    tlh.marked_limit IN ('Yes', 'Does not apply') AND
                                    tlh.visible_traceability IN ('Yes', 'Does not apply') AND
                                    tlh.hook_type IN ('Yes', 'Does not apply') AND
                                    tlh.marked_grade IN ('Yes', 'Does not apply') AND
                                    tlh.legible_identification IN ('Yes', 'Does not apply') AND
                                    tlh.cracks IN ('Yes', 'Does not apply') AND
                                    tlh.dents IN ('Yes', 'Does not apply') AND
                                    tlh.excessive_corrosion IN ('Yes', 'Does not apply') AND
                                    tlh.visible_deformations IN ('Yes', 'Does not apply') AND
                                    tlh.overheating IN ('Yes', 'Does not apply') AND
                                    tlh.weld_splatter IN ('Yes', 'Does not apply') AND
                                    tlh.unauthorized_modifications IN ('Yes', 'Does not apply') AND
                                    tlh.damages_thread IN ('Yes', 'Does not apply') AND
                                    tlh.throat_limits IN ('Yes', 'Does not apply') AND
                                    tlh.opening_deformations IN ('Yes', 'Does not apply') AND
                                    tlh.excessive_wear_area IN ('Yes', 'Does not apply') AND
                                    tlh.sharp_edges IN ('Yes', 'Does not apply') AND
                                    tlh.widening_tip IN ('Yes', 'Does not apply') AND
                                    tlh.bearing_wear IN ('Yes', 'Does not apply') AND
                                    tlh.impact_mark IN ('Yes', 'Does not apply') AND
                                    tlh.hook_shape IN ('Yes', 'Does not apply') AND
                                    tlh.intact_latch IN ('Yes', 'Does not apply') AND
                                    tlh.correctly_latch IN ('Yes', 'Does not apply') AND
                                    tlh.tension_latch IN ('Yes', 'Does not apply') AND
                                    tlh.deformations_latch IN ('Yes', 'Does not apply') AND
                                    tlh.exessive_wear_points IN ('Yes', 'Does not apply') AND
                                    tlh.opening_latch IN ('Yes', 'Does not apply') AND
                                    tlh.corrosion_latch IN ('Yes', 'Does not apply') AND
                                    tlh.damages_latch IN ('Yes', 'Does not apply') AND
                                    tlh.hook_rotation IN ('Yes', 'Does not apply') AND
                                    tlh.locking_mechanism IN ('Yes', 'Does not apply') AND
                                    tlh.smooth_joints IN ('Yes', 'Does not apply') AND
                                    tlh.jamming IN ('Yes', 'Does not apply') AND
                                    tlh.automatic_latch IN ('Yes', 'Does not apply') AND
                                    tlh.excessive_play IN ('Yes', 'Does not apply') AND
                                    tlh.hook_dimensions IN ('Yes', 'Does not apply') AND
                                    tlh.reduction_wear IN ('Yes', 'Does not apply') AND
                                    tlh.throat_opening IN ('Yes', 'Does not apply') AND
                                    tlh.elongation IN ('Yes', 'Does not apply') AND
                                    tlh.angular_deformations IN ('Yes', 'Does not apply') AND
                                    tlh.rigging_hook_acceptance IN ('Yes', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tlm.type = 'Master Link' AND
                                    tll.rigging_plan IN ('Yes', 'Does not apply') AND
                                    tll.rigging_items IN ('Yes', 'Does not apply') AND
                                    tll.rigging_material IN ('Yes', 'Does not apply') AND
                                    tll.rigging_condition IN ('Yes', 'Does not apply') AND
                                    tll.visible_mark IN ('Yes', 'Does not apply') AND
                                    tll.marked_limit IN ('Yes', 'Does not apply') AND
                                    tll.marked_dimension IN ('Yes', 'Does not apply') AND
                                    tll.marked_grade IN ('Yes', 'Does not apply') AND
                                    tll.visible_traceability IN ('Yes', 'Does not apply') AND
                                    tll.cracks IN ('Yes', 'Does not apply') AND
                                    tll.wear IN ('Yes', 'Does not apply') AND
                                    tll.corrosion IN ('Yes', 'Does not apply') AND
                                    tll.visible_deformations IN ('Yes', 'Does not apply') AND
                                    tll.overheating IN ('Yes', 'Does not apply') AND
                                    tll.weld_splatter IN ('Yes', 'Does not apply') AND
                                    tll.modifications IN ('Yes', 'Does not apply') AND
                                    tll.stretching IN ('Yes', 'Does not apply') AND
                                    tll.original_shape IN ('Yes', 'Does not apply') AND
                                    tll.contact_deformations IN ('Yes', 'Does not apply') AND
                                    tll.sharp_edges IN ('Yes', 'Does not apply') AND
                                    tll.impact_mark IN ('Yes', 'Does not apply') AND
                                    tll.section_reduction IN ('Yes', 'Does not apply') AND
                                    tll.deep_scratches IN ('Yes', 'Does not apply') AND
                                    tll.tolerated_dimensions IN ('Yes', 'Does not apply') AND
                                    tll.reduction_wear IN ('No', 'Does not apply') AND
                                    tll.elongation IN ('Yes', 'Does not apply') AND
                                    tll.angular_deformations IN ('Yes', 'Does not apply') AND
                                    tll.rigging_link_acceptance IN ('Yes', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tlm.type = 'Shackles' AND
                                    tls.rigging_plan IN ('Yes', 'Does not apply') AND
                                    tls.rigging_items IN ('Yes', 'Does not apply') AND
                                    tls.rigging_material IN ('Yes', 'Does not apply') AND
                                    tls.rigging_condition IN ('Yes', 'Does not apply') AND
                                    tls.visible_mark IN ('Yes', 'Does not apply') AND
                                    tls.visible_grade_number IN ('Yes', 'Does not apply') AND
                                    tls.visible_limit IN ('Yes', 'Does not apply') AND
                                    tls.visible_pin_mark IN ('Yes', 'Does not apply') AND
                                    tls.visible_grade_material IN ('Yes', 'Does not apply') AND
                                    tls.compatible_pin IN ('Yes', 'Does not apply') AND
                                    tls.fractures IN ('No', 'Does not apply') AND
                                    tls.deformations IN ('No', 'Does not apply') AND
                                    tls.corrosion IN ('No', 'Does not apply') AND
                                    tls.wear IN ('No', 'Does not apply') AND
                                    tls.notches IN ('No', 'Does not apply') AND
                                    tls.overheating IN ('No', 'Does not apply') AND
                                    tls.bends IN ('No', 'Does not apply') AND
                                    tls.shackle_pin IN ('Yes', 'Does not apply') AND
                                    tls.tightened_pin IN ('Yes', 'Does not apply') AND
                                    tls.present_pin IN ('Yes', 'Does not apply') AND
                                    tls.rigging_shackles_acceptance IN ('Yes', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tlm.type = 'Spreader' AND
                                    tlsp.rigging_plan IN ('Yes', 'Does not apply') AND
                                    tlsp.rigging_items IN ('Yes', 'Does not apply') AND
                                    tlsp.rigging_material IN ('Yes', 'Does not apply') AND
                                    tlsp.rigging_condition IN ('Yes', 'Does not apply') AND
                                    tlsp.marked_limit IN ('Yes', 'Does not apply') AND
                                    tlsp.marked_weight IN ('Yes', 'Does not apply') AND
                                    tlsp.main_fractures IN ('No', 'Does not apply') AND
                                    tlsp.permanent_deformations IN ('No', 'Does not apply') AND
                                    tlsp.corrosion IN ('No', 'Does not apply') AND
                                    tlsp.damages_collision IN ('No', 'Does not apply') AND
                                    tlsp.twisting IN ('No', 'Does not apply') AND
                                    tlsp.overheating IN ('No', 'Does not apply') AND
                                    tlsp.improper_repair IN ('No', 'Does not apply') AND
                                    tlsp.contact_wear IN ('No', 'Does not apply') AND
                                    tlsp.lifting_deformations IN ('Yes', 'Does not apply') AND
                                    tlsp.lifting_wear IN ('No', 'Does not apply') AND
                                    tlsp.weld_fractures IN ('No', 'Does not apply') AND
                                    tlsp.hole_deformations IN ('No', 'Does not apply') AND
                                    tlsp.present_safety_devices IN ('Yes', 'Does not apply') AND
                                    tlsp.adjustment_mechanisms IN ('Yes', 'Does not apply') AND
                                    tlsp.present_pin IN ('Yes', 'Does not apply') AND
                                    tlsp.excessive_wear IN ('No', 'Does not apply') AND
                                    tlsp.visible_mark IN ('Yes', 'Does not apply') AND
                                    tlsp.components_deformations IN ('No', 'Does not apply') AND
                                    tlsp.locking_devices IN ('Yes', 'Does not apply') AND
                                    tlsp.components_obstructions IN ('Yes', 'Does not apply') AND
                                    tlsp.rigging_spreader_acceptance IN ('Yes', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tlm.type = 'Synthetic Sling' AND
                                    tlsl.rigging_plan IN ('Yes', 'Does not apply') AND
                                    tlsl.rigging_items IN ('Yes', 'Does not apply') AND
                                    tlsl.rigging_material IN ('Yes', 'Does not apply') AND
                                    tlsl.rigging_condition IN ('Yes', 'Does not apply') AND
                                    tlsl.missing_label IN ('No', 'Does not apply') AND
                                    tlsl.visible_capacity IN ('No', 'Does not apply') AND
                                    tlsl.core_exposure IN ('No', 'Does not apply') AND
                                    tlsl.core_cut IN ('No', 'Does not apply') AND
                                    tlsl.core_broken IN ('No', 'Does not apply') AND
                                    tlsl.core_abrasion IN ('No', 'Does not apply') AND
                                    tlsl.damages_protection IN ('No', 'Does not apply') AND
                                    tlsl.cut_any IN ('No', 'Does not apply') AND
                                    tlsl.cut_sides IN ('No', 'Does not apply') AND
                                    tlsl.punctures IN ('No', 'Does not apply') AND
                                    tlsl.abrasion IN ('No', 'Does not apply') AND
                                    tlsl.damages_heat IN ('No', 'Does not apply') AND
                                    tlsl.excessive_friction IN ('No', 'Does not apply') AND
                                    tlsl.knots IN ('No', 'Does not apply') AND
                                    tlsl.modifications IN ('No', 'Does not apply') AND
                                    tlsl.chemical_stains IN ('No', 'Does not apply') AND
                                    tlsl.overload IN ('No', 'Does not apply') AND
                                    tlsl.hardware_deformations IN ('No', 'Does not apply') AND
                                    tlsl.wear_metal IN ('No', 'Does not apply') AND
                                    tlsl.fractures IN ('No', 'Does not apply') AND
                                    tlsl.hook_deformations IN ('No', 'Does not apply') AND
                                    tlsl.rigging_sling_acceptance IN ('Yes', 'Does not apply')
                                THEN 1 
                                WHEN 
                                    tlm.type = 'Wire Ropes' AND
                                    tlw.rigging_plan IN ('Yes', 'Does not apply') AND
                                    tlw.rigging_items IN ('Yes', 'Does not apply') AND
                                    tlw.rigging_material IN ('Yes', 'Does not apply') AND
                                    tlw.rigging_condition IN ('Yes', 'Does not apply') AND
                                    tlw.broken_wires IN ('No', 'Does not apply') AND
                                    tlw.broken_wires_concentration IN ('No', 'Does not apply') AND
                                    tlw.broken_wires_terminal IN ('No', 'Does not apply') AND
                                    tlw.broken_wires_valley IN ('No', 'Does not apply') AND
                                    tlw.wear_wires_reduction IN ('No', 'Does not apply') AND
                                    tlw.wear_wires_localized IN ('No', 'Does not apply') AND
                                    tlw.wear_wires_uniform IN ('No', 'Does not apply') AND
                                    tlw.corrosion_wires_visible IN ('No', 'Does not apply') AND
                                    tlw.corrosion_wires_signs IN ('No', 'Does not apply') AND
                                    tlw.corrosion_wires_cavities IN ('No', 'Does not apply') AND
                                    tlw.deformation_wires_crushing IN ('No', 'Does not apply') AND
                                    tlw.deformation_wires_caging IN ('No', 'Does not apply') AND
                                    tlw.deformation_wires_protusion IN ('No', 'Does not apply') AND
                                    tlw.deformation_wires_knots IN ('No', 'Does not apply') AND
                                    tlw.deformation_wires_flattening IN ('No', 'Does not apply') AND
                                    tlw.other_wires_heat IN ('No', 'Does not apply') AND
                                    tlw.other_wires_electrical IN ('No', 'Does not apply') AND
                                    tlw.other_wires_strands IN ('No', 'Does not apply') AND
                                    tlw.other_wires_exposed IN ('No', 'Does not apply') AND
                                    tlw.other_wires_terminal IN ('No', 'Does not apply') AND
                                    tlw.lubrification_wires_lack IN ('No', 'Does not apply') AND
                                    tlw.lubrification_wires_drying IN ('No', 'Does not apply') AND
                                    tlw.conclusion_wires_suitable IN ('Yes', 'Does not apply') AND
                                    tlw.rigging_wires_acceptance IN ('Yes', 'Does not apply')
                                THEN 1 
                                ELSE 0 
                            END
                        ) = COUNT(*)
                    THEN 'Good'
                    ELSE 'Bad'
                END AS lifting_condition
            FROM tbl_lifting_material tlm 
            LEFT JOIN tbl_task_survey_boarding ttsb 
                ON ttsb.id_task = tlm.id_task 
            LEFT JOIN tbl_lifting_chain tlc
                ON tlc.id_lifting_material  = tlm.id_lifting_material AND tlm.type = 'Chain'
            LEFT JOIN tbl_lifting_hook tlh
                ON tlh.id_lifting_material = tlm.id_lifting_material AND tlm.type = 'Hook'
            LEFT JOIN tbl_lifting_link tll
                ON tll.id_lifting_material = tlm.id_lifting_material AND tlm.type = 'Master Link'
            LEFT JOIN tbl_lifting_shackles tls
                ON tls.id_lifting_material = tlm.id_lifting_material AND tlm.type = 'Shackles'
            LEFT JOIN tbl_lifting_spreader tlsp
                ON tlsp.id_lifting_material = tlm.id_lifting_material AND tlm.type = 'Spreader'
            LEFT JOIN tbl_lifting_sling tlsl
                ON tlsl.id_lifting_material = tlm.id_lifting_material AND tlm.type = 'Synthetic Sling'
            LEFT JOIN tbl_lifting_wire tlw 
                ON tlw.id_lifting_material = tlm.id_lifting_material AND tlm.type = 'Wire Ropes'
            WHERE ttsb.id_survey = :demanda_id;
        """

        result = current_session.execute(
            text(query),
            {"demanda_id": demanda_id}
        ).mappings()

        row = result.fetchone()

        if not row:
            return None, f"Demanda ID {demanda_id} not found."

        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        data = {
            "lifting_condition": safe(row.get("lifting_condition")),
        }

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on demanda_id {demanda_id}")
        return None, str(e)
    finally:
        current_session.close()