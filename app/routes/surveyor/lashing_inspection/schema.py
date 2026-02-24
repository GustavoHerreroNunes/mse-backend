from app import ma
from app.utils.base_schema import BaseSchema

class LashingInspectionChainSchema(BaseSchema):
    class Meta:
        primary_key = "id_lashing_material"
        fields = (
            "id_lashing_material", "lashing_plan", "lashing_items", "lashing_material",
            "lashing_condition", "visible_mark", "marked_grade", "marked_limit",
            "visible_traceability", "specified_length", "sling_number", "legible_identification",
            "marked_inspection", "links_cracks", "excessive_wear", "links_stretched",
            "links_twisted", "corrosion", "overheating", "weld_splatter", "links_obstructions",
            "links_diameter", "reduction_wear", "elongation_length", "lashing_chain_acceptance"
        )

    id_lashing_material = ma.Integer(required=True)
    lashing_plan = ma.String(required=False)
    lashing_items = ma.String(required=False)
    lashing_material = ma.String(required=False)
    lashing_condition = ma.String(required=False)
    visible_mark = ma.String(required=False)
    marked_grade = ma.String(required=False)
    marked_limit = ma.String(required=False)
    visible_traceability = ma.String(required=False)
    specified_length = ma.String(required=False)
    sling_number = ma.String(required=False)
    legible_identification = ma.String(required=False)
    marked_inspection = ma.String(required=False)
    links_cracks = ma.String(required=False)
    excessive_wear = ma.String(required=False)
    links_stretched = ma.String(required=False)
    links_twisted = ma.String(required=False)
    corrosion = ma.String(required=False)
    overheating = ma.String(required=False)
    weld_splatter = ma.String(required=False)
    links_obstructions = ma.String(required=False)
    links_diameter = ma.String(required=False)
    reduction_wear = ma.String(required=False)
    elongation_length = ma.String(required=False)
    lashing_chain_acceptance = ma.String(required=False)

lashing_chain_schema = LashingInspectionChainSchema()
lashing_chain_list_schema = LashingInspectionChainSchema(many=True)

class LashingInspectionShacklesSchema(BaseSchema):
    class Meta:
        primary_key = "id_lashing_material"
        fields = (
            "id_lashing_material", "lashing_plan", "lashing_items", "lashing_material",
            "lashing_condition", "visible_mark", "visible_grade_number", "visible_limit",
            "visible_pin_mark", "visible_grade_material", "compatible_pin", "fractures",
            "deformations", "corrosion", "wear", "notches", "overheating", "bends",
            "shackle_pin", "tightened_pin", "present_pin", "lashing_shackles_acceptance"
        )

    id_lashing_material = ma.Integer(required=True)
    lashing_plan = ma.String(required=False)
    lashing_items = ma.String(required=False)
    lashing_material = ma.String(required=False)
    lashing_condition = ma.String(required=False)
    visible_mark = ma.String(required=False)
    visible_grade_number = ma.String(required=False)
    visible_limit = ma.String(required=False)
    visible_pin_mark = ma.String(required=False)
    visible_grade_material = ma.String(required=False)
    compatible_pin = ma.String(required=False)
    fractures = ma.String(required=False)
    deformations = ma.String(required=False)
    corrosion = ma.String(required=False)
    wear = ma.String(required=False)
    notches = ma.String(required=False)
    overheating = ma.String(required=False)
    bends = ma.String(required=False)
    shackle_pin = ma.String(required=False)
    tightened_pin = ma.String(required=False)
    present_pin = ma.String(required=False)
    lashing_shackles_acceptance = ma.String(required=False)

lashing_shackles_schema = LashingInspectionShacklesSchema()
lashing_shackles_list_schema = LashingInspectionShacklesSchema(many=True)

class LashingInspectionLinesSchema(BaseSchema):
    class Meta:
        primary_key = "id_lashing_material"
        fields = (
            "id_lashing_material", "lashing_plan", "lashing_items", "lashing_material",
            "lashing_condition", "missing_label", "visible_capacity", "core_exposure",
            "core_cut", "core_broken", "core_abrasion", "damages_protection", "cut_any",
            "cut_sides", "punctures", "abrasion", "damages_heat", "excessive_friction",
            "knots", "modifications", "chemical_stains", "overload", "hardware_deformations",
            "wear_metal", "fractures", "hook_deformations", "lashing_lines_acceptance"
        )

    id_lashing_material = ma.Integer(required=True)
    lashing_plan = ma.String(required=False)
    lashing_items = ma.String(required=False)
    lashing_material = ma.String(required=False)
    lashing_condition = ma.String(required=False)
    missing_label = ma.String(required=False)
    visible_capacity = ma.String(required=False)
    core_exposure = ma.String(required=False)
    core_cut = ma.String(required=False)
    core_broken = ma.String(required=False)
    core_abrasion = ma.String(required=False)
    damages_protection = ma.String(required=False)
    cut_any = ma.String(required=False)
    cut_sides = ma.String(required=False)
    punctures = ma.String(required=False)
    abrasion = ma.String(required=False)
    damages_heat = ma.String(required=False)
    excessive_friction = ma.String(required=False)
    knots = ma.String(required=False)
    modifications = ma.String(required=False)
    chemical_stains = ma.String(required=False)
    overload = ma.String(required=False)
    hardware_deformations = ma.String(required=False)
    wear_metal = ma.String(required=False)
    fractures = ma.String(required=False)
    hook_deformations = ma.String(required=False)
    lashing_lines_acceptance = ma.String(required=False)

lashing_lines_schema = LashingInspectionLinesSchema()
lashing_lines_list_schema = LashingInspectionLinesSchema(many=True)

class LashingInspectionWireSchema(BaseSchema):
    class Meta:
        primary_key = "id_lashing_material"
        fields = (
            "id_lashing_material", "lashing_plan", "lashing_items", "lashing_material",
            "lashing_condition", "broken_wires", "broken_wires_concentration",
            "broken_wires_terminal", "broken_wires_valley", "wear_wires_reduction",
            "wear_wires_localized", "wear_wires_uniform", "corrosion_wires_visible",
            "corrosion_wires_signs", "corrosion_wires_cavities", "deformation_wires_crushing",
            "deformation_wires_caging", "deformation_wires_protusion", "deformation_wires_knots",
            "deformation_wires_flattening", "other_wires_heat", "other_wires_electrical",
            "other_wires_strands", "other_wires_exposed", "other_wires_terminal",
            "lubrification_wires_lack", "lubrification_wires_drying", "conclusion_wires_suitable",
            "lashing_wires_acceptance"
        )

    id_lashing_material = ma.Integer(required=True)
    lashing_plan = ma.String(required=False)
    lashing_items = ma.String(required=False)
    lashing_material = ma.String(required=False)
    lashing_condition = ma.String(required=False)
    broken_wires = ma.String(required=False)
    broken_wires_concentration = ma.String(required=False)
    broken_wires_terminal = ma.String(required=False)
    broken_wires_valley = ma.String(required=False)
    wear_wires_reduction = ma.String(required=False)
    wear_wires_localized = ma.String(required=False)
    wear_wires_uniform = ma.String(required=False)
    corrosion_wires_visible = ma.String(required=False)
    corrosion_wires_signs = ma.String(required=False)
    corrosion_wires_cavities = ma.String(required=False)
    deformation_wires_crushing = ma.String(required=False)
    deformation_wires_caging = ma.String(required=False)
    deformation_wires_protusion = ma.String(required=False)
    deformation_wires_knots = ma.String(required=False)
    deformation_wires_flattening = ma.String(required=False)
    other_wires_heat = ma.String(required=False)
    other_wires_electrical = ma.String(required=False)
    other_wires_strands = ma.String(required=False)
    other_wires_exposed = ma.String(required=False)
    other_wires_terminal = ma.String(required=False)
    lubrification_wires_lack = ma.String(required=False)
    lubrification_wires_drying = ma.String(required=False)
    conclusion_wires_suitable = ma.String(required=False)
    lashing_wires_acceptance = ma.String(required=False)

lashing_wire_schema = LashingInspectionWireSchema()
lashing_wire_list_schema = LashingInspectionWireSchema(many=True)

class LashingInspectionStopperSchema(BaseSchema):
    class Meta:
        primary_key = "id_lashing_material"
        fields = (
            "id_lashing_material", "lashing_plan", "lashing_items", "lashing_material",
            "lashing_condition", "dimensions", "wear", "twisted", "corrosion", 
            "lashing_stopper_acceptance"
        )

    id_lashing_material = ma.Integer(required=True)
    lashing_plan = ma.String(required=False)
    lashing_items = ma.String(required=False)
    lashing_material = ma.String(required=False)
    lashing_condition = ma.String(required=False)
    dimensions = ma.String(required=False)
    wear = ma.String(required=False)
    twisted = ma.String(required=False)
    corrosion = ma.String(required=False)
    lashing_stopper_acceptance = ma.String(required=False)

lashing_stopper_schema = LashingInspectionStopperSchema()
lashing_stopper_list_schema = LashingInspectionStopperSchema(many=True)

class LashingInspectionTensionerSchema(BaseSchema):
    class Meta:
        primary_key = "id_lashing_material"
        fields = (
            "id_lashing_material", "lashing_plan", "lashing_items", "lashing_material",
            "lashing_condition", "visible_mark", "legible_identification", "marked_limit",
            "visible_traceability", "cracks", "wear", "stretched", "twisted", "corrosion",
            "overheating", "lashing_tensioner_acceptance"
        )

    id_lashing_material = ma.Integer(required=True)
    lashing_plan = ma.String(required=False)
    lashing_items = ma.String(required=False)
    lashing_material = ma.String(required=False)
    lashing_condition = ma.String(required=False)
    visible_mark = ma.String(required=False)
    legible_identification = ma.String(required=False)
    marked_limit = ma.String(required=False)
    visible_traceability = ma.String(required=False)
    cracks = ma.String(required=False)
    wear = ma.String(required=False)
    stretched = ma.String(required=False)
    twisted = ma.String(required=False)
    corrosion = ma.String(required=False)
    overheating = ma.String(required=False)
    lashing_tensioner_acceptance = ma.String(required=False)

lashing_tensioner_schema = LashingInspectionTensionerSchema()
lashing_tensioner_list_schema = LashingInspectionTensionerSchema(many=True)