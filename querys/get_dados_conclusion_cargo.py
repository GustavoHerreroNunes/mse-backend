from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_ia_conclusion_cargo(demanda_id):
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
                                    tc.cargo_type = 'Wooden Crate' AND
                                    tcc.well_received IN ('Yes', 'Does not apply') AND
                                    tcc.instruction IN ('Yes', 'Does not apply') AND
                                    tcc.external_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.packing IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.identification_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.protection IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.stability IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.cleanliness IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.integrity IN ('Yes', 'Does not apply') AND
                                    tcc.warning_labels IN ('Yes', 'Does not apply') AND
                                    tcc.markings IN ('Yes', 'Does not apply') AND
                                    tcc.moisture IN ('No', 'Does not apply') AND
                                    tcc.weight_distribution IN ('Yes', 'Does not apply') AND
                                    tcc.stacking IN ('Yes', 'Does not apply') AND
                                    tcc.shifting IN ('No', 'Does not apply') AND
                                    tccw.breakage IN ('No', 'Does not apply') AND
                                    tccw.moisture IN ('No', 'Does not apply') AND
                                    tccw.infestation IN ('No', 'Does not apply')
                                THEN 1 
                                WHEN 
                                    tc.cargo_type = 'Metallic' AND
                                    tcc.well_received IN ('Yes', 'Does not apply') AND
                                    tcc.instruction IN ('Yes', 'Does not apply') AND
                                    tcc.external_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.packing IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.identification_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.protection IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.stability IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.cleanliness IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.integrity IN ('Yes', 'Does not apply') AND
                                    tcc.warning_labels IN ('Yes', 'Does not apply') AND
                                    tcc.markings IN ('Yes', 'Does not apply') AND
                                    tcc.moisture IN ('No', 'Does not apply') AND
                                    tcc.weight_distribution IN ('Yes', 'Does not apply') AND
                                    tcc.stacking IN ('Yes', 'Does not apply') AND
                                    tcc.shifting IN ('No', 'Does not apply') AND
                                    tccm.corrosion IN ('No', 'Does not apply') AND
                                    tccm.deformation IN ('No', 'Does not apply') AND
                                    tccm.scratches IN ('No', 'Does not apply') AND
                                    tccm.damages_weld IN ('No', 'Does not apply') AND
                                    tccm.pitting_marks IN ('No', 'Does not apply') AND
                                    tccm.chemical_traces IN ('No', 'Does not apply') AND
                                    tccm.heat_marks IN ('No', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tc.cargo_type = 'Bale or Bagged' AND
                                    tcc.well_received IN ('Yes', 'Does not apply') AND
                                    tcc.instruction IN ('Yes', 'Does not apply') AND
                                    tcc.external_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.packing IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.identification_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.protection IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.stability IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.cleanliness IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.integrity IN ('Yes', 'Does not apply') AND
                                    tcc.warning_labels IN ('Yes', 'Does not apply') AND
                                    tcc.markings IN ('Yes', 'Does not apply') AND
                                    tcc.moisture IN ('No', 'Does not apply') AND
                                    tcc.weight_distribution IN ('Yes', 'Does not apply') AND
                                    tcc.stacking IN ('Yes', 'Does not apply') AND
                                    tcc.shifting IN ('No', 'Does not apply') AND
                                    tccb.tears IN ('No', 'Does not apply') AND
                                    tccb.moisture IN ('No', 'Does not apply') AND
                                    tccb.contamination IN ('No', 'Does not apply') AND
                                    tccb.deformation IN ('No', 'Does not apply') AND
                                    tccb.strapping IN ('No', 'Does not apply') AND
                                    tccb.expected_cargo IN ('No', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tc.cargo_type = 'Reel' AND
                                    tcc.well_received IN ('Yes', 'Does not apply') AND
                                    tcc.instruction IN ('Yes', 'Does not apply') AND
                                    tcc.external_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.packing IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.identification_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.protection IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.stability IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.cleanliness IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.integrity IN ('Yes', 'Does not apply') AND
                                    tcc.warning_labels IN ('Yes', 'Does not apply') AND
                                    tcc.markings IN ('Yes', 'Does not apply') AND
                                    tcc.moisture IN ('No', 'Does not apply') AND
                                    tcc.weight_distribution IN ('Yes', 'Does not apply') AND
                                    tcc.stacking IN ('Yes', 'Does not apply') AND
                                    tcc.shifting IN ('No', 'Does not apply') and
                                    tccr.corrosion IN ('No', 'Does not apply') and
                                    tccr.deformation_berth IN ('No', 'Does not apply') and
                                    tccr.deformation_lifting IN ('No', 'Does not apply') and
                                    tccr.deformation_lashing IN ('No', 'Does not apply') and
                                    tccr.tears IN ('No', 'Does not apply') and
                                    tccr.heat_marks IN ('No', 'Does not apply') and
                                    tccr.damages_weld IN ('No', 'Does not apply') and
                                    tccr.scratches IN ('No', 'Does not apply') and
                                    tccr.pitting_marks IN ('No', 'Does not apply') and
                                    tccr.damages_pipe IN ('No', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tc.cargo_type = 'Machinery' AND
                                    tcc.well_received IN ('Yes', 'Does not apply') AND
                                    tcc.instruction IN ('Yes', 'Does not apply') AND
                                    tcc.external_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.packing IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.identification_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.protection IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.stability IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.cleanliness IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.integrity IN ('Yes', 'Does not apply') AND
                                    tcc.warning_labels IN ('Yes', 'Does not apply') AND
                                    tcc.markings IN ('Yes', 'Does not apply') AND
                                    tcc.moisture IN ('No', 'Does not apply') AND
                                    tcc.weight_distribution IN ('Yes', 'Does not apply') AND
                                    tcc.stacking IN ('Yes', 'Does not apply') AND
                                    tcc.shifting IN ('No', 'Does not apply') and
                                    tccma.damages_mechanical IN ('No', 'Does not apply') and
                                    tccma.broken_wires IN ('No', 'Does not apply') and
                                    tccma.leaks IN ('No', 'Does not apply') and
                                    tccma.corrosion IN ('No', 'Does not apply') and
                                    tccma.broken_hydraulic IN ('No', 'Does not apply') and
                                    tccma.broken_control IN ('No', 'Does not apply') and
                                    tccma.broken_gauges IN ('No', 'Does not apply') and
                                    tccma.scratches IN ('No', 'Does not apply')
                                THEN 1
                                WHEN 
                                    tc.cargo_type = 'Steel Pipes' AND
                                    tcc.well_received IN ('Yes', 'Does not apply') AND
                                    tcc.instruction IN ('Yes', 'Does not apply') AND
                                    tcc.external_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.packing IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.identification_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.protection IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.stability IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.cleanliness IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.integrity IN ('Yes', 'Does not apply') AND
                                    tcc.warning_labels IN ('Yes', 'Does not apply') AND
                                    tcc.markings IN ('Yes', 'Does not apply') AND
                                    tcc.moisture IN ('No', 'Does not apply') AND
                                    tcc.weight_distribution IN ('Yes', 'Does not apply') AND
                                    tcc.stacking IN ('Yes', 'Does not apply') AND
                                    tcc.shifting IN ('No', 'Does not apply') and
                                    tccs.denting IN ('No', 'Does not apply') and
                                    tccs.ovality IN ('No', 'Does not apply') and
                                    tccs.corrosion IN ('No', 'Does not apply') and
                                    tccs.damages_end IN ('No', 'Does not apply') and
                                    tccs.damages_coating IN ('No', 'Does not apply') and
                                    tccs.scratches IN ('No', 'Does not apply') and
                                    tccs.endcaps IN ('No', 'Does not apply')
                                THEN 1 
                                WHEN 
                                    tc.cargo_type = 'Xtree or THD' AND
                                    tcc.well_received IN ('Yes', 'Does not apply') AND
                                    tcc.instruction IN ('Yes', 'Does not apply') AND
                                    tcc.external_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.packing IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.identification_condition IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.protection IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.stability IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.cleanliness IN ('Very Good', 'Good', 'Fair', 'Does not apply') AND
                                    tcc.integrity IN ('Yes', 'Does not apply') AND
                                    tcc.warning_labels IN ('Yes', 'Does not apply') AND
                                    tcc.markings IN ('Yes', 'Does not apply') AND
                                    tcc.moisture IN ('No', 'Does not apply') AND
                                    tcc.weight_distribution IN ('Yes', 'Does not apply') AND
                                    tcc.stacking IN ('Yes', 'Does not apply') AND
                                    tcc.shifting IN ('No', 'Does not apply') and
                                    tcct.damages_mechanical IN ('No', 'Does not apply') and
                                    tcct.broken_wires IN ('No', 'Does not apply') and
                                    tcct.leaks IN ('No', 'Does not apply') and
                                    tcct.corrosion IN ('No', 'Does not apply') and
                                    tcct.broken_hydraulic IN ('No', 'Does not apply') and
                                    tcct.broken_control IN ('No', 'Does not apply') and
                                    tcct.broken_gauges IN ('No', 'Does not apply') and
                                    tcct.coating IN ('No', 'Does not apply') and
                                    tcct.broken_anodes IN ('No', 'Does not apply') and
                                    tcct.tarphauling IN ('No', 'Does not apply') and
                                    tcct.broken_lashing IN ('No', 'Does not apply') and
                                    tcct.elements_order IN ('No', 'Does not apply')
                                THEN 1 
                                ELSE 0 
                            END
                        ) = COUNT(*)
                    THEN 'Good'
                    ELSE 'Bad'
                END AS cargo_condition
            FROM tbl_cargo tc
            LEFT JOIN tbl_cargo_condition tcc 
                ON tcc.cargo_id = tc.cargo_id
            LEFT JOIN tbl_task_survey_boarding ttsb 
                ON ttsb.id_task = tc.id_task
            LEFT JOIN tbl_cargo_condition_wood tccw
                ON tccw.cargo_id = tc.cargo_id AND tc.cargo_type = 'Wooden Crate'
            LEFT JOIN tbl_cargo_condition_metallic tccm
                ON tccm.cargo_id = tc.cargo_id AND tc.cargo_type = 'Metallic'
            LEFT JOIN tbl_cargo_condition_bale tccb
                ON tccb.cargo_id = tc.cargo_id AND tc.cargo_type = 'Bale or Bagged'
            LEFT JOIN tbl_cargo_condition_reel tccr
                ON tccr.cargo_id = tc.cargo_id AND tc.cargo_type = 'Reel'
            LEFT JOIN tbl_cargo_condition_machinery tccma
                ON tccma.cargo_id = tc.cargo_id AND tc.cargo_type = 'Machinery'
            LEFT JOIN tbl_cargo_condition_steel tccs
                ON tccs.cargo_id = tc.cargo_id AND tc.cargo_type = 'Steel Pipes'
            LEFT JOIN tbl_cargo_condition_thd tcct
                ON tcct.cargo_id = tc.cargo_id AND tc.cargo_type = 'Xtree or THD'
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
            "cargo_condition": safe(row.get("cargo_condition"))
        }

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on demanda_id {demanda_id}")
        return None, str(e)
    finally:
        current_session.close()