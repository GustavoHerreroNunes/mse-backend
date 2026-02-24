from app import ma
from app.utils.base_schema import BaseSchema

class CargoInspectionWoodSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "breakage", "ranking_breakage", "moisture",
            "ranking_moisture", "infestation", "ranking_infestation"
        )

    cargo_id = ma.Integer(required=True)
    breakage = ma.String(required=False)
    ranking_breakage = ma.String(required=False)
    moisture = ma.String(required=False)
    ranking_moisture = ma.String(required=False)
    infestation = ma.String(required=False)
    ranking_infestation = ma.String(required=False)

cargo_wood_schema = CargoInspectionWoodSchema()
cargo_wood_list_schema = CargoInspectionWoodSchema(many=True)

class CargoInspectionBaleSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "tears", "ranking_tears", "moisture",
            "ranking_moisture", "contamination", "ranking_contamination",
            "deformation", "ranking_deformation", "strapping",
            "ranking_strapping", "expected_cargo", "ranking_expected_cargo"
        )

    cargo_id = ma.Integer(required=True)
    tears = ma.String(required=False)
    ranking_tears = ma.String(required=False)
    moisture = ma.String(required=False)
    ranking_moisture = ma.String(required=False)
    contamination = ma.String(required=False)
    ranking_contamination = ma.String(required=False)
    deformation = ma.String(required=False)
    ranking_deformation = ma.String(required=False)
    strapping = ma.String(required=False)
    ranking_strapping = ma.String(required=False)
    expected_cargo = ma.String(required=False)
    ranking_expected_cargo = ma.String(required=False)

cargo_bale_schema = CargoInspectionBaleSchema()
cargo_bale_list_schema = CargoInspectionBaleSchema(many=True)

class CargoInspectionMachinerySchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "damages_mechanical", "ranking_damages_mechanical", "broken_wires",
            "ranking_broken_wires", "leaks", "ranking_leaks", "corrosion",
            "ranking_corrosion", "broken_hydraulic", "ranking_broken_hydraulic",
            "broken_control", "ranking_broken_control", "broken_gauges",
            "ranking_broken_gauges", "scratches", "ranking_scratches"
        )

    cargo_id = ma.Integer(required=True)
    damages_mechanical = ma.String(required=False)
    ranking_damages_mechanical = ma.String(required=False)
    broken_wires = ma.String(required=False)
    ranking_broken_wires = ma.String(required=False)
    leaks = ma.String(required=False)
    ranking_leaks = ma.String(required=False)
    corrosion = ma.String(required=False)
    ranking_corrosion = ma.String(required=False)
    broken_hydraulic = ma.String(required=False)
    ranking_broken_hydraulic = ma.String(required=False)
    broken_control = ma.String(required=False)
    ranking_broken_control = ma.String(required=False)
    broken_gauges = ma.String(required=False)
    ranking_broken_gauges = ma.String(required=False)
    scratches = ma.String(required=False)
    ranking_scratches = ma.String(required=False)

cargo_machinery_schema = CargoInspectionMachinerySchema()
cargo_machinery_list_schema = CargoInspectionMachinerySchema(many=True)

class CargoInspectionMetallicSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "corrosion", "ranking_corrosion", "deformation",
            "ranking_deformation", "scratches", "ranking_scratches",
            "damages_weld", "ranking_damages_weld", "pitting_marks",
            "ranking_pitting_marks", "chemical_traces", "ranking_chemical_traces",
            "heat_marks", "ranking_heat_marks"
        )

    cargo_id = ma.Integer(required=True)
    corrosion = ma.String(required=False)
    ranking_corrosion = ma.String(required=False)
    deformation = ma.String(required=False)
    ranking_deformation = ma.String(required=False)
    scratches = ma.String(required=False)
    ranking_scratches = ma.String(required=False)
    damages_weld = ma.String(required=False)
    ranking_damages_weld = ma.String(required=False)
    pitting_marks = ma.String(required=False)
    ranking_pitting_marks = ma.String(required=False)
    chemical_traces = ma.String(required=False)
    ranking_chemical_traces = ma.String(required=False)
    heat_marks = ma.String(required=False)
    ranking_heat_marks = ma.String(required=False)

cargo_metallic_schema = CargoInspectionMetallicSchema()
cargo_metallic_list_schema = CargoInspectionMetallicSchema(many=True)

class CargoInspectionReelSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "corrosion", "ranking_corrosion", "deformation_berth",
            "ranking_deformation_berth", "deformation_lifting", "ranking_deformation_lifting",
            "deformation_lashing", "ranking_deformation_lashing", "tears",
            "ranking_tears", "heat_marks", "ranking_heat_marks", "damages_weld",
            "ranking_damages_weld", "scratches", "ranking_scratches", "pitting_marks",
            "ranking_pitting_marks", "damages_pipe", "ranking_damages_pipe"
        )

    cargo_id = ma.Integer(required=True)
    corrosion = ma.String(required=False)
    ranking_corrosion = ma.String(required=False)
    deformation_berth = ma.String(required=False)
    ranking_deformation_berth = ma.String(required=False)
    deformation_lifting = ma.String(required=False)
    ranking_deformation_lifting = ma.String(required=False)
    deformation_lashing = ma.String(required=False)
    ranking_deformation_lashing = ma.String(required=False)
    tears = ma.String(required=False)
    ranking_tears = ma.String(required=False)
    heat_marks = ma.String(required=False)
    ranking_heat_marks = ma.String(required=False)
    damages_weld = ma.String(required=False)
    ranking_damages_weld = ma.String(required=False)
    scratches = ma.String(required=False)
    ranking_scratches = ma.String(required=False)
    pitting_marks = ma.String(required=False)
    ranking_pitting_marks = ma.String(required=False)
    damages_pipe = ma.String(required=False)
    ranking_damages_pipe = ma.String(required=False)

cargo_reel_schema = CargoInspectionReelSchema()
cargo_reel_list_schema = CargoInspectionReelSchema(many=True)

class CargoInspectionSteelSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "denting", "ranking_denting", "ovality", "ranking_ovality",
            "corrosion", "ranking_corrosion", "damages_end", "ranking_damages_end",
            "damages_coating", "ranking_damages_coating", "scratches", "ranking_scratches",
            "endcaps", "ranking_endcaps"
        )

    cargo_id = ma.Integer(required=True)
    denting = ma.String(required=False)
    ranking_denting = ma.String(required=False)
    ovality = ma.String(required=False)
    ranking_ovality = ma.String(required=False)
    corrosion = ma.String(required=False)
    ranking_corrosion = ma.String(required=False)
    damages_end = ma.String(required=False)
    ranking_damages_end = ma.String(required=False)
    damages_coating = ma.String(required=False)
    ranking_damages_coating = ma.String(required=False)
    scratches = ma.String(required=False)
    ranking_scratches = ma.String(required=False)
    endcaps = ma.String(required=False)
    ranking_endcaps = ma.String(required=False)

cargo_steel_schema = CargoInspectionSteelSchema()
cargo_steel_list_schema = CargoInspectionSteelSchema(many=True)

class CargoInspectionTHDSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "damages_mechanical", "ranking_damages_mechanical", "broken_wires",
            "ranking_broken_wires", "leaks", "ranking_leaks", "corrosion", "ranking_corrosion",
            "broken_hydraulic", "ranking_broken_hydraulic", "broken_control", "ranking_broken_control",
            "broken_gauges", "ranking_broken_gauges", "coating", "ranking_coating",
            "broken_anodes", "ranking_broken_anodes", "tarphauling", "ranking_tarphauling",
            "broken_lashing", "ranking_broken_lashing", "elements_order", "ranking_elements_order"
        )

    cargo_id = ma.Integer(required=True)
    damages_mechanical = ma.String(required=False)
    ranking_damages_mechanical = ma.String(required=False)
    broken_wires = ma.String(required=False)
    ranking_broken_wires = ma.String(required=False)
    leaks = ma.String(required=False)
    ranking_leaks = ma.String(required=False)
    corrosion = ma.String(required=False)
    ranking_corrosion = ma.String(required=False)
    broken_hydraulic = ma.String(required=False)
    ranking_broken_hydraulic = ma.String(required=False)
    broken_control = ma.String(required=False)
    ranking_broken_control = ma.String(required=False)
    broken_gauges = ma.String(required=False)
    ranking_broken_gauges = ma.String(required=False)
    coating = ma.String(required=False)
    ranking_coating = ma.String(required=False)
    broken_anodes = ma.String(required=False)
    ranking_broken_anodes = ma.String(required=False)
    tarphauling = ma.String(required=False)
    ranking_tarphauling = ma.String(required=False)
    broken_lashing = ma.String(required=False)
    ranking_broken_lashing = ma.String(required=False)
    elements_order = ma.String(required=False)
    ranking_elements_order = ma.String(required=False)

cargo_thd_schema = CargoInspectionTHDSchema()
cargo_thd_list_schema = CargoInspectionTHDSchema(many=True)