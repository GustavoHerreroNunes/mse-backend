from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_ia_conclusion_lashing(demanda_id):
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
                                    tlm.type = 'Chain' AND
                                    tlc.lashing_plan IN ('Yes', 'Does not apply') AND
                                    tlc.lashing_items IN ('Yes', 'Does not apply') AND
                                    tlc.lashing_material IN ('Yes', 'Does not apply') AND
                                    tlc.lashing_condition IN ('Yes', 'Does not apply') AND
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
                                    tlc.lashing_chain_acceptance IN ('Yes', 'Does not apply')
                                THEN 1 
                                WHEN 
                                    tlm.type = 'Shackles' AND
                                    tls.lashing_plan IN ('Yes', 'Does not apply') AND
                                    tls.lashing_items IN ('Yes', 'Does not apply') AND
                                    tls.lashing_material IN ('Yes', 'Does not apply') AND
                                    tls.lashing_condition IN ('Yes', 'Does not apply') AND
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
                                    tls.lashing_shackles_acceptance IN ('Yes', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tlm.type = 'Synthetic Lines' AND
                                    tll.lashing_plan IN ('Yes', 'Does not apply') AND
                                    tll.lashing_items IN ('Yes', 'Does not apply') AND
                                    tll.lashing_material IN ('Yes', 'Does not apply') AND
                                    tll.lashing_condition IN ('Yes', 'Does not apply') AND
                                    tll.missing_label IN ('No', 'Does not apply') AND
                                    tll.visible_capacity IN ('No', 'Does not apply') AND
                                    tll.core_exposure IN ('No', 'Does not apply') AND
                                    tll.core_cut IN ('No', 'Does not apply') AND
                                    tll.core_broken IN ('No', 'Does not apply') AND
                                    tll.core_abrasion IN ('No', 'Does not apply') AND
                                    tll.damages_protection IN ('No', 'Does not apply') AND
                                    tll.cut_any IN ('No', 'Does not apply') AND
                                    tll.cut_sides IN ('No', 'Does not apply') AND
                                    tll.punctures IN ('No', 'Does not apply') AND
                                    tll.abrasion IN ('No', 'Does not apply') AND
                                    tll.damages_heat IN ('No', 'Does not apply') AND
                                    tll.excessive_friction IN ('No', 'Does not apply') AND
                                    tll.knots IN ('No', 'Does not apply') AND
                                    tll.modifications IN ('No', 'Does not apply') AND
                                    tll.chemical_stains IN ('No', 'Does not apply') AND
                                    tll.overload IN ('No', 'Does not apply') AND
                                    tll.hardware_deformations IN ('No', 'Does not apply') AND
                                    tll.wear_metal IN ('No', 'Does not apply') AND
                                    tll.fractures IN ('No', 'Does not apply') AND
                                    tll.hook_deformations IN ('No', 'Does not apply') AND
                                    tll.lashing_lines_acceptance IN ('Yes', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tlm.type = 'Stopper, dog plate' AND
                                    tlst.lashing_plan IN ('Yes', 'Does not apply') AND
                                    tlst.lashing_items IN ('Yes', 'Does not apply') AND
                                    tlst.lashing_material IN ('Yes', 'Does not apply') AND
                                    tlst.lashing_condition IN ('Yes', 'Does not apply') AND
                                    tlst.dimensions IN ('Yes', 'Does not apply') AND
                                    tlst.wear IN ('Yes', 'Does not apply') AND
                                    tlst.twisted IN ('Yes', 'Does not apply') AND
                                    tlst.corrosion IN ('Yes', 'Does not apply') AND
                                    tlst.lashing_stopper_acceptance IN ('Yes', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tlm.type = 'Tensioner, turnbuckle, arm lever' AND
                                    tlt.lashing_plan IN ('Yes', 'Does not apply') AND
                                    tlt.lashing_items IN ('Yes', 'Does not apply') AND
                                    tlt.lashing_material IN ('Yes', 'Does not apply') AND
                                    tlt.lashing_condition IN ('Yes', 'Does not apply') AND
                                    tlt.visible_mark IN ('Yes', 'Does not apply') AND
                                    tlt.legible_identification IN ('Yes', 'Does not apply') AND
                                    tlt.marked_limit IN ('Yes', 'Does not apply') AND
                                    tlt.visible_traceability IN ('Yes', 'Does not apply') AND
                                    tlt.cracks IN ('Yes', 'Does not apply') AND
                                    tlt.wear IN ('Yes', 'Does not apply') AND
                                    tlt.stretched IN ('Yes', 'Does not apply') AND
                                    tlt.twisted IN ('Yes', 'Does not apply') AND
                                    tlt.corrosion IN ('Yes', 'Does not apply') AND
                                    tlt.overheating IN ('Yes', 'Does not apply') AND
                                    tlt.lashing_tensioner_acceptance IN ('Yes', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tlm.type = 'Wire Ropes' AND
                                    tlw.lashing_plan IN ('Yes', 'Does not apply') AND
                                    tlw.lashing_items IN ('Yes', 'Does not apply') AND
                                    tlw.lashing_material IN ('Yes', 'Does not apply') AND
                                    tlw.lashing_condition IN ('Yes', 'Does not apply') AND
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
                                    tlw.lashing_wires_acceptance IN ('Yes', 'Does not apply')
                                THEN 1 
                                ELSE 0 
                            END
                        ) = COUNT(*)
                    THEN 'Good'
                    ELSE 'Bad'
                END AS lashing_condition
            FROM tbl_lashing_material tlm 
            LEFT JOIN tbl_task_survey_boarding ttsb 
                ON ttsb.id_task = tlm.id_task 
            LEFT JOIN tbl_lashing_chain tlc
                ON tlc.id_lashing_material  = tlm.id_lashing_material AND tlm.type = 'Chain'
            LEFT JOIN tbl_lashing_shackles tls
                ON tls.id_lashing_material = tlm.id_lashing_material AND tlm.type = 'Shackles'
            LEFT JOIN tbl_lashing_lines tll
                ON tll.id_lashing_material = tlm.id_lashing_material AND tlm.type = 'Synthetic Lines'
            LEFT JOIN tbl_lashing_stopper tlst
                ON tlst.id_lashing_material = tlm.id_lashing_material AND tlm.type = 'Stopper, dog plate'
            LEFT JOIN tbl_lashing_tensioner tlt
                ON tlt.id_lashing_material = tlm.id_lashing_material AND tlm.type = 'Tensioner, turnbuckle, arm lever'
            LEFT JOIN tbl_lashing_wire tlw
                ON tlw.id_lashing_material = tlm.id_lashing_material AND tlm.type = 'Wire Ropes'
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
            "lashing_condition": safe(row.get("lashing_condition")),
        }

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on demanda_id {demanda_id}")
        return None, str(e)
    finally:
        current_session.close()