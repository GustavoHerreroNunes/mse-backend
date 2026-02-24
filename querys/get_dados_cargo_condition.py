from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_cargo_condition(cargo_id, cargo_type):
    current_session = Session()
    print('get_dados_table')

    try:
        if cargo_type == "Wooden Crate":
            query = """
                select 
                    tcc.external_condition,
                    tcc.packing,
                    tcc.identification_condition,
                    tcc.protection,
                    tcc.stability,
                    tcc.cleanliness,
                    tcc.integrity,
                    tcc.warning_labels,
                    tcc.markings,
                    tcc.moisture,
                    tcc.weight_distribution,
                    tcc.stacking,
                    tcc.shifting,
                    tccw.ranking_breakage,
                    tccw.ranking_moisture,
                    tccw.ranking_infestation
                from Tbl_cargo_condition tcc
                left join tbl_cargo_condition_wood tccw on tccw.cargo_id = tcc.cargo_id
                where tcc.cargo_id = :cargo_id
            """
        elif cargo_type == "Steel Pipes":
            query = """
                select 
                    tcc.external_condition,
                    tcc.packing,
                    tcc.identification_condition,
                    tcc.protection,
                    tcc.stability,
                    tcc.cleanliness,
                    tcc.integrity,
                    tcc.warning_labels,
                    tcc.markings,
                    tcc.moisture,
                    tcc.weight_distribution,
                    tcc.stacking,
                    tcc.shifting,
                    tccs.ranking_denting,
                    tccs.ranking_ovality,
                    tccs.ranking_corrosion,
                    tccs.ranking_damages_end,
                    tccs.ranking_damages_coating,
                    tccs.ranking_scratches,
                    tccs.ranking_endcaps
                from Tbl_cargo_condition tcc
                left join tbl_cargo_condition_steel tccs on tccs.cargo_id = tcc.cargo_id
                where tcc.cargo_id = :cargo_id
            """
        elif cargo_type == "Machinery":
            query = """
                select 
                    tcc.external_condition,
                    tcc.packing,
                    tcc.identification_condition,
                    tcc.protection,
                    tcc.stability,
                    tcc.cleanliness,
                    tcc.integrity,
                    tcc.warning_labels,
                    tcc.markings,
                    tcc.moisture,
                    tcc.weight_distribution,
                    tcc.stacking,
                    tcc.shifting,
                    tccm.ranking_damages_mechanical,
                    tccm.ranking_broken_wires,
                    tccm.ranking_leaks,
                    tccm.ranking_corrosion,
                    tccm.ranking_broken_hydraulic,
                    tccm.ranking_broken_control,
                    tccm.ranking_broken_gauges,
                    tccm.ranking_scratches
                from Tbl_cargo_condition tcc
                left join tbl_cargo_condition_machinery tccm on tccm.cargo_id = tcc.cargo_id
                where tcc.cargo_id = :cargo_id
            """
        elif cargo_type == "Xtree or THD":
            query = """
                select 
                    tcc.external_condition,
                    tcc.packing,
                    tcc.identification_condition,
                    tcc.protection,
                    tcc.stability,
                    tcc.cleanliness,
                    tcc.integrity,
                    tcc.warning_labels,
                    tcc.markings,
                    tcc.moisture,
                    tcc.weight_distribution,
                    tcc.stacking,
                    tcc.shifting,
                    tcct.ranking_damages_mechanical,
                    tcct.ranking_broken_wires,
                    tcct.ranking_leaks,
                    tcct.ranking_corrosion,
                    tcct.ranking_broken_hydraulic,
                    tcct.ranking_broken_control,
                    tcct.ranking_broken_gauges,
                    tcct.ranking_coating,
                    tcct.ranking_broken_anodes,
                    tcct.ranking_tarphauling,
                    tcct.ranking_broken_lashing,
                    tcct.ranking_elements_order
                from Tbl_cargo_condition tcc
                left join tbl_cargo_condition_thd tcct on tcct.cargo_id = tcc.cargo_id
                where tcc.cargo_id = :cargo_id
            """
        elif cargo_type == "Bale or Bagged":
            query = """
                select 
                    tcc.external_condition,
                    tcc.packing,
                    tcc.identification_condition,
                    tcc.protection,
                    tcc.stability,
                    tcc.cleanliness,
                    tcc.integrity,
                    tcc.warning_labels,
                    tcc.markings,
                    tcc.moisture,
                    tcc.weight_distribution,
                    tcc.stacking,
                    tcc.shifting,
                    tccb.ranking_tears,
                    tccb.ranking_moisture,
                    tccb.ranking_contamination,
                    tccb.ranking_deformation,
                    tccb.ranking_strapping,
                    tccb.ranking_expected_cargo
                from Tbl_cargo_condition tcc
                left join tbl_cargo_condition_bale tccb on tccb.cargo_id = tcc.cargo_id
                where tcc.cargo_id = :cargo_id
            """
        elif cargo_type == "Metallic":
            query = """
                select 
                    tcc.external_condition,
                    tcc.packing,
                    tcc.identification_condition,
                    tcc.protection,
                    tcc.stability,
                    tcc.cleanliness,
                    tcc.integrity,
                    tcc.warning_labels,
                    tcc.markings,
                    tcc.moisture,
                    tcc.weight_distribution,
                    tcc.stacking,
                    tcc.shifting,
                    tccm.ranking_corrosion,
                    tccm.ranking_deformation,
                    tccm.ranking_scratches,
                    tccm.ranking_damages_weld,
                    tccm.ranking_pitting_marks,
                    tccm.ranking_chemical_traces,
                    tccm.ranking_heat_marks
                from Tbl_cargo_condition tcc
                left join tbl_cargo_condition_metallic tccm on tccm.cargo_id = tcc.cargo_id
                where tcc.cargo_id = :cargo_id
            """
        elif cargo_type == "Reel":
            query = """
                select 
                    tcc.external_condition,
                    tcc.packing,
                    tcc.identification_condition,
                    tcc.protection,
                    tcc.stability,
                    tcc.cleanliness,
                    tcc.integrity,
                    tcc.warning_labels,
                    tcc.markings,
                    tcc.moisture,
                    tcc.weight_distribution,
                    tcc.stacking,
                    tcc.shifting,
                    tccr.ranking_corrosion,
                    tccr.ranking_deformation_berth,
                    tccr.ranking_deformation_lifting,
                    tccr.ranking_deformation_lashing,
                    tccr.ranking_tears,
                    tccr.ranking_heat_marks,
                    tccr.ranking_damages_weld,
                    tccr.ranking_scratches,
                    tccr.ranking_pitting_marks,
                    tccr.ranking_damages_pipe
                from Tbl_cargo_condition tcc
                left join tbl_cargo_condition_reel tccr on tccr.cargo_id = tcc.cargo_id
                where tcc.cargo_id = 18
            """
        else:
            return None, f"Unsupported cargo_type: {cargo_type}"
        
        result = current_session.execute(
            text(query),
            {"cargo_id": cargo_id}
        ).mappings()

        rows = result.fetchall()

        if not rows:
            return None, f"Cargo ID {cargo_id} not found."

        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        if cargo_type == "Wooden Crate":
            row = rows[0]
            data = {
                "external_condition": safe(row.get("external_condition")),
                "packing": safe(row.get("packing")),
                "identification_condition": safe(row.get("identification_condition")),
                "protection": safe(row.get("protection")),
                "stability": safe(row.get("stability")),
                "cleanliness": safe(row.get("cleanliness")),
                "integrity": safe(row.get("integrity")),
                "warning_labels": safe(row.get("warning_labels")),
                "markings": safe(row.get("markings")),
                "moisture": safe(row.get("moisture")),
                "weight_distribution": safe(row.get("weight_distribution")),
                "stacking": safe(row.get("stacking")),
                "shifting": safe(row.get("shifting")),
                "ranking_breakage": safe(row.get("ranking_breakage")),
                "ranking_moisture": safe(row.get("ranking_moisture")),
                "ranking_infestation": safe(row.get("ranking_infestation"))
            }
        elif cargo_type == "Steel Pipes":
            row = rows[0]
            data = {
                "external_condition": safe(row.get("external_condition")),
                "packing": safe(row.get("packing")),
                "identification_condition": safe(row.get("identification_condition")),
                "protection": safe(row.get("protection")),
                "stability": safe(row.get("stability")),
                "cleanliness": safe(row.get("cleanliness")),
                "integrity": safe(row.get("integrity")),
                "warning_labels": safe(row.get("warning_labels")),
                "markings": safe(row.get("markings")),
                "moisture": safe(row.get("moisture")),
                "weight_distribution": safe(row.get("weight_distribution")),
                "stacking": safe(row.get("stacking")),
                "shifting": safe(row.get("shifting")),
                "ranking_denting": safe(row.get("ranking_denting")),
                "ranking_ovality": safe(row.get("ranking_ovality")),
                "ranking_corrosion": safe(row.get("ranking_corrosion")),
                "ranking_damages_end": safe(row.get("ranking_damages_end")),
                "ranking_damages_coating": safe(row.get("ranking_damages_coating")),
                "ranking_scratches": safe(row.get("ranking_scratches")),
                "ranking_endcaps": safe(row.get("ranking_endcaps"))
            }
        elif cargo_type == "Machinery":
            row = rows[0]
            data = {
                "external_condition": safe(row.get("external_condition")),
                "packing": safe(row.get("packing")),
                "identification_condition": safe(row.get("identification_condition")),
                "protection": safe(row.get("protection")),
                "stability": safe(row.get("stability")),
                "cleanliness": safe(row.get("cleanliness")),
                "integrity": safe(row.get("integrity")),
                "warning_labels": safe(row.get("warning_labels")),
                "markings": safe(row.get("markings")),
                "moisture": safe(row.get("moisture")),
                "weight_distribution": safe(row.get("weight_distribution")),
                "stacking": safe(row.get("stacking")),
                "shifting": safe(row.get("shifting")),
                "ranking_damages_mechanical": safe(row.get("ranking_damages_mechanical")),
                "ranking_broken_wires": safe(row.get("ranking_broken_wires")),
                "ranking_leaks": safe(row.get("ranking_leaks")),
                "ranking_corrosion": safe(row.get("ranking_corrosion")),
                "ranking_broken_hydraulic": safe(row.get("ranking_broken_hydraulic")),
                "ranking_broken_control": safe(row.get("ranking_broken_control")),
                "ranking_broken_gauges": safe(row.get("ranking_broken_gauges")),
                "ranking_scratches": safe(row.get("ranking_scratches"))
            }
        elif cargo_type == "Xtree or THD":
            row = rows[0]
            data = {
                "external_condition": safe(row.get("external_condition")),
                "packing": safe(row.get("packing")),
                "identification_condition": safe(row.get("identification_condition")),
                "protection": safe(row.get("protection")),
                "stability": safe(row.get("stability")),
                "cleanliness": safe(row.get("cleanliness")),
                "integrity": safe(row.get("integrity")),
                "warning_labels": safe(row.get("warning_labels")),
                "markings": safe(row.get("markings")),
                "moisture": safe(row.get("moisture")),
                "weight_distribution": safe(row.get("weight_distribution")),
                "stacking": safe(row.get("stacking")),
                "shifting": safe(row.get("shifting")),
                "ranking_damages_mechanical": safe(row.get("ranking_damages_mechanical")),
                "ranking_broken_wires": safe(row.get("ranking_broken_wires")),
                "ranking_leaks": safe(row.get("ranking_leaks")),
                "ranking_corrosion": safe(row.get("ranking_corrosion")),
                "ranking_broken_hydraulic": safe(row.get("ranking_broken_hydraulic")),
                "ranking_broken_control": safe(row.get("ranking_broken_control")),
                "ranking_broken_gauges": safe(row.get("ranking_broken_gauges")),
                "ranking_coating": safe(row.get("ranking_coating")),
                "ranking_broken_anodes": safe(row.get("ranking_broken_anodes")),
                "ranking_tarphauling": safe(row.get("ranking_tarphauling")),
                "ranking_broken_lashing": safe(row.get("ranking_broken_lashing")),
                "ranking_elements_order": safe(row.get("ranking_elements_order"))
            }
        elif cargo_type == "Bale or Bagged":
            row = rows[0]
            data = {
                "external_condition": safe(row.get("external_condition")),
                "packing": safe(row.get("packing")),
                "identification_condition": safe(row.get("identification_condition")),
                "protection": safe(row.get("protection")),
                "stability": safe(row.get("stability")),
                "cleanliness": safe(row.get("cleanliness")),
                "integrity": safe(row.get("integrity")),
                "warning_labels": safe(row.get("warning_labels")),
                "markings": safe(row.get("markings")),
                "moisture": safe(row.get("moisture")),
                "weight_distribution": safe(row.get("weight_distribution")),
                "stacking": safe(row.get("stacking")),
                "shifting": safe(row.get("shifting")),
                "ranking_tears": safe(row.get("ranking_tears")),
                "ranking_moisture": safe(row.get("ranking_moisture")),
                "ranking_contamination": safe(row.get("ranking_contamination")),
                "ranking_deformation": safe(row.get("ranking_deformation")),
                "ranking_strapping": safe(row.get("ranking_strapping")),
                "ranking_expected_cargo": safe(row.get("ranking_expected_cargo"))
            }
        elif cargo_type == "Metallic":
            row = rows[0]
            data = {
                "external_condition": safe(row.get("external_condition")),
                "packing": safe(row.get("packing")),
                "identification_condition": safe(row.get("identification_condition")),
                "protection": safe(row.get("protection")),
                "stability": safe(row.get("stability")),
                "cleanliness": safe(row.get("cleanliness")),
                "integrity": safe(row.get("integrity")),
                "warning_labels": safe(row.get("warning_labels")),
                "markings": safe(row.get("markings")),
                "moisture": safe(row.get("moisture")),
                "weight_distribution": safe(row.get("weight_distribution")),
                "stacking": safe(row.get("stacking")),
                "shifting": safe(row.get("shifting")),
                "ranking_corrosion": safe(row.get("ranking_corrosion")),
                "ranking_deformation": safe(row.get("ranking_deformation")),
                "ranking_scratches": safe(row.get("ranking_scratches")),
                "ranking_damages_weld": safe(row.get("ranking_damages_weld")),
                "ranking_pitting_marks": safe(row.get("ranking_pitting_marks")),
                "ranking_chemical_traces": safe(row.get("ranking_chemical_traces")),
                "ranking_heat_marks": safe(row.get("ranking_heat_marks"))
            }
        elif cargo_type == "Reel":
            row = rows[0]
            data = {
                "external_condition": safe(row.get("external_condition")),
                "packing": safe(row.get("packing")),
                "identification_condition": safe(row.get("identification_condition")),
                "protection": safe(row.get("protection")),
                "stability": safe(row.get("stability")),
                "cleanliness": safe(row.get("cleanliness")),
                "integrity": safe(row.get("integrity")),
                "warning_labels": safe(row.get("warning_labels")),
                "markings": safe(row.get("markings")),
                "moisture": safe(row.get("moisture")),
                "weight_distribution": safe(row.get("weight_distribution")),
                "stacking": safe(row.get("stacking")),
                "shifting": safe(row.get("shifting")),
                "ranking_corrosion": safe(row.get("ranking_corrosion")),
                "ranking_deformation_berth": safe(row.get("ranking_deformation_berth")),
                "ranking_deformation_lifting": safe(row.get("ranking_deformation_lifting")),
                "ranking_deformation_lashing": safe(row.get("ranking_deformation_lashing")),
                "ranking_tears": safe(row.get("ranking_tears")),
                "ranking_heat_marks": safe(row.get("ranking_heat_marks")),
                "ranking_damages_weld": safe(row.get("ranking_damages_weld")),
                "ranking_scratches": safe(row.get("ranking_scratches")),
                "ranking_pitting_marks": safe(row.get("ranking_pitting_marks")),
                "ranking_damages_pipe": safe(row.get("ranking_damages_pipe"))
            }
        else:
            return None, f"Unsupported cargo_type: {cargo_type}"

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on cargo_id {cargo_id}")
        return None, str(e)
    finally:
        current_session.close()