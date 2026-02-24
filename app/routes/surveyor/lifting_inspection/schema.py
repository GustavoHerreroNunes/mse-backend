from app import ma
from app.utils.base_schema import BaseSchema

class LiftingInspectionChainSchema(BaseSchema):
    class Meta:
        primary_key = "id_lifting_material"
        fields = (
            "id_lifting_material", "rigging_plan", "rigging_items", "rigging_material",
            "rigging_condition", "visible_mark", "marked_grade", "marked_limit",
            "visible_traceability", "specified_length", "sling_number", "legible_identification",
            "marked_inspection", "links_cracks", "excessive_wear", "links_stretched",
            "links_twisted", "corrosion", "overheating", "weld_splatter", "links_obstructions",
            "links_diameter", "reduction_wear", "elongation_length", "rigging_chain_acceptance"
        )

    id_lifting_material = ma.Integer(required=True)
    rigging_plan = ma.String(required=False)
    rigging_items = ma.String(required=False)
    rigging_material = ma.String(required=False)
    rigging_condition = ma.String(required=False)
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
    rigging_chain_acceptance = ma.String(required=False)

lifting_chain_schema = LiftingInspectionChainSchema()
lifting_chain_list_schema = LiftingInspectionChainSchema(many=True)

class LiftingInspectionHookSchema(BaseSchema):
    class Meta:
        primary_key = "id_lifting_material"
        fields = (
            "id_lifting_material", "rigging_plan", "rigging_items", "rigging_material",
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
        )

    id_lifting_material = ma.Integer(required=True)
    rigging_plan = ma.String(required=False)
    rigging_items = ma.String(required=False)
    rigging_material = ma.String(required=False)
    rigging_condition = ma.String(required=False)
    visible_mark = ma.String(required=False)
    marked_limit = ma.String(required=False)
    visible_traceability = ma.String(required=False)
    hook_type = ma.String(required=False)
    marked_grade = ma.String(required=False)
    legible_identification = ma.String(required=False)
    cracks = ma.String(required=False)
    dents = ma.String(required=False)
    excessive_corrosion = ma.String(required=False)
    visible_deformations = ma.String(required=False)
    overheating = ma.String(required=False)
    weld_splatter = ma.String(required=False)
    unauthorized_modifications = ma.String(required=False)
    damages_thread = ma.String(required=False)
    throat_limits = ma.String(required=False)
    opening_deformations = ma.String(required=False)
    excessive_wear_area = ma.String(required=False)
    sharp_edges = ma.String(required=False)
    widening_tip = ma.String(required=False)
    bearing_wear = ma.String(required=False)
    impact_mark = ma.String(required=False)
    hook_shape = ma.String(required=False)
    intact_latch = ma.String(required=False)
    correctly_latch = ma.String(required=False)
    tension_latch = ma.String(required=False)
    deformations_latch = ma.String(required=False)
    exessive_wear_points = ma.String(required=False)
    opening_latch = ma.String(required=False)
    corrosion_latch = ma.String(required=False)
    damages_latch = ma.String(required=False)
    hook_rotation = ma.String(required=False)
    locking_mechanism = ma.String(required=False)
    smooth_joints = ma.String(required=False)
    jamming = ma.String(required=False)
    automatic_latch = ma.String(required=False)
    excessive_play = ma.String(required=False)
    hook_dimensions = ma.String(required=False)
    reduction_wear = ma.String(required=False)
    throat_opening = ma.String(required=False)
    elongation = ma.String(required=False)
    angular_deformations = ma.String(required=False)
    rigging_hook_acceptance = ma.String(required=False)

lifting_hook_schema = LiftingInspectionHookSchema()
lifting_hook_list_schema = LiftingInspectionHookSchema(many=True)

class LiftingInspectionLinkSchema(BaseSchema):
    class Meta:
        primary_key = "id_lifting_material"
        fields = (
            "id_lifting_material", "rigging_plan", "rigging_items", "rigging_material",
            "rigging_condition", "visible_mark", "marked_limit", "marked_dimension",
            "marked_grade", "visible_traceability", "cracks", "wear", "corrosion",
            "visible_deformations", "overheating", "weld_splatter", "modifications",
            "stretching", "original_shape", "contact_deformations", "sharp_edges", "impact_mark",
            "section_reduction", "deep_scratches", "tolerated_dimensions", "reduction_wear",
            "elongation", "angular_deformations", "rigging_link_acceptance"
        )

    id_lifting_material = ma.Integer(required=True)
    rigging_plan = ma.String(required=False)
    rigging_items = ma.String(required=False)
    rigging_material = ma.String(required=False)
    rigging_condition = ma.String(required=False)
    visible_mark = ma.String(required=False)
    marked_limit = ma.String(required=False)
    marked_dimension = ma.String(required=False)
    marked_grade = ma.String(required=False)
    visible_traceability = ma.String(required=False)
    cracks = ma.String(required=False)
    wear = ma.String(required=False)
    corrosion = ma.String(required=False)
    visible_deformations = ma.String(required=False)
    overheating = ma.String(required=False)
    weld_splatter = ma.String(required=False)
    modifications = ma.String(required=False)
    stretching = ma.String(required=False)
    original_shape = ma.String(required=False)
    contact_deformations = ma.String(required=False)
    sharp_edges = ma.String(required=False)
    impact_mark = ma.String(required=False)
    section_reduction = ma.String(required=False)
    deep_scratches = ma.String(required=False)
    tolerated_dimensions = ma.String(required=False)
    reduction_wear = ma.String(required=False)
    elongation = ma.String(required=False)
    angular_deformations = ma.String(required=False)
    rigging_link_acceptance = ma.String(required=False)

lifting_link_schema = LiftingInspectionLinkSchema()
lifting_link_list_schema = LiftingInspectionLinkSchema(many=True)

class LiftingInspectionShacklesSchema(BaseSchema):
    class Meta:
        primary_key = "id_lifting_material"
        fields = (
            "id_lifting_material", "rigging_plan", "rigging_items", "rigging_material",
            "rigging_condition", "visible_mark", "visible_grade_number", "visible_limit",
            "visible_pin_mark", "visible_grade_material", "compatible_pin", "fractures",
            "deformations", "corrosion", "wear", "notches", "overheating", "bends",
            "shackle_pin", "tightened_pin", "present_pin", "rigging_shackles_acceptance"
        )

    id_lifting_material = ma.Integer(required=True)
    rigging_plan = ma.String(required=False)
    rigging_items = ma.String(required=False)
    rigging_material = ma.String(required=False)
    rigging_condition = ma.String(required=False)
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
    rigging_shackles_acceptance = ma.String(required=False)

lifting_shackles_schema = LiftingInspectionShacklesSchema()
lifting_shackles_list_schema = LiftingInspectionShacklesSchema(many=True)

class LiftingInspectionSlingSchema(BaseSchema):
    class Meta:
        primary_key = "id_lifting_material"
        fields = (
            "id_lifting_material", "rigging_plan", "rigging_items", "rigging_material",
            "rigging_condition", "missing_label", "visible_capacity", "core_exposure",
            "core_cut", "core_broken", "core_abrasion", "damages_protection", "cut_any",
            "cut_sides", "punctures", "abrasion", "damages_heat", "excessive_friction",
            "knots", "modifications", "chemical_stains", "overload", "hardware_deformations",
            "wear_metal", "fractures", "hook_deformations", "rigging_sling_acceptance"
        )

    id_lifting_material = ma.Integer(required=True)
    rigging_plan = ma.String(required=False)
    rigging_items = ma.String(required=False)
    rigging_material = ma.String(required=False)
    rigging_condition = ma.String(required=False)
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
    rigging_sling_acceptance = ma.String(required=False)

lifting_sling_schema = LiftingInspectionSlingSchema()
lifting_sling_list_schema = LiftingInspectionSlingSchema(many=True)

class LiftingInspectionSpreaderSchema(BaseSchema):
    class Meta:
        primary_key = "id_lifting_material"
        fields = (
            "id_lifting_material", "rigging_plan", "rigging_items", "rigging_material",
            "rigging_condition", "marked_limit", "marked_weight", "main_fractures",
            "permanent_deformations", "corrosion", "damages_collision", "twisting",
            "overheating", "improper_repair", "contact_wear", "lifting_deformations",
            "lifting_wear", "weld_fractures", "hole_deformations", "present_safety_devices",
            "adjustment_mechanisms", "present_pin", "excessive_wear", "visible_mark",
            "components_deformations", "locking_devices", "components_obstructions",
            "rigging_spreader_acceptance"
        )

    id_lifting_material = ma.Integer(required=True)
    rigging_plan = ma.String(required=False)
    rigging_items = ma.String(required=False)
    rigging_material = ma.String(required=False)
    rigging_condition = ma.String(required=False)
    marked_limit = ma.String(required=False)
    marked_weight = ma.String(required=False)
    main_fractures = ma.String(required=False)
    permanent_deformations = ma.String(required=False)
    corrosion = ma.String(required=False)
    damages_collision = ma.String(required=False)
    twisting = ma.String(required=False)
    overheating = ma.String(required=False)
    improper_repair = ma.String(required=False)
    contact_wear = ma.String(required=False)
    lifting_deformations = ma.String(required=False)
    lifting_wear = ma.String(required=False)
    weld_fractures = ma.String(required=False)
    hole_deformations = ma.String(required=False)
    present_safety_devices = ma.String(required=False)
    adjustment_mechanisms = ma.String(required=False)
    present_pin = ma.String(required=False)
    excessive_wear = ma.String(required=False)
    visible_mark = ma.String(required=False)
    components_deformations = ma.String(required=False)
    locking_devices = ma.String(required=False)
    components_obstructions = ma.String(required=False)
    rigging_spreader_acceptance = ma.String(required=False)

lifting_spreader_schema = LiftingInspectionSpreaderSchema()
lifting_spreader_list_schema = LiftingInspectionSpreaderSchema(many=True)

class LiftingInspectionWireSchema(BaseSchema):
    class Meta:
        primary_key = "id_lifting_material"
        fields = (
            "id_lifting_material", "rigging_plan", "rigging_items", "rigging_material",
            "rigging_condition", "broken_wires", "broken_wires_concentration",
            "broken_wires_terminal", "broken_wires_valley", "wear_wires_reduction",
            "wear_wires_localized", "wear_wires_uniform", "corrosion_wires_visible",
            "corrosion_wires_signs", "corrosion_wires_cavities", "deformation_wires_crushing",
            "deformation_wires_caging", "deformation_wires_protusion", "deformation_wires_knots",
            "deformation_wires_flattening", "other_wires_heat", "other_wires_electrical",
            "other_wires_strands", "other_wires_exposed", "other_wires_terminal",
            "lubrification_wires_lack", "lubrification_wires_drying", "conclusion_wires_suitable",
            "rigging_wires_acceptance"
        )

    id_lifting_material = ma.Integer(required=True)
    rigging_plan = ma.String(required=False)
    rigging_items = ma.String(required=False)
    rigging_material = ma.String(required=False)
    rigging_condition = ma.String(required=False)
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
    rigging_wires_acceptance = ma.String(required=False)

lifting_wire_schema = LiftingInspectionWireSchema()
lifting_wire_list_schema = LiftingInspectionWireSchema(many=True)