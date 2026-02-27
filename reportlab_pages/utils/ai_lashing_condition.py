import json
import logging
import re
from reportlab_pages.utils.gemini_client import prompt_model

# Mapeamento de colunas para descrições legíveis – Wire Ropes
FIELD_DESCRIPTIONS_WIRE = {
    "lashing_plan": "Applied Lashing arrangement is the same as the issued Lashing plan.",
    "lashing_items": "Lashing item certificates have been issued and verified. They are valid.",
    "lashing_material": "All Lashing materials show visible capacity and are in accordance with the Lashing plan.",
    "lashing_condition": "General condition of Lashing materials is suitable for their intended purpose.",
    "broken_wires": "Broken wires exceed the quantity allowed by the standard (in one lay length or in 6 times the rope diameter).",
    "broken_wires_concentration": "There is a concentration of broken wires in a single strand of the rope.",
    "broken_wires_terminal": "Broken wires are present near terminals or connections.",
    "broken_wires_valley": "Broken wires are found in the valleys between the strands.",
    "wear_wires_reduction": "Rope diameter has reduced by more than 10% of the nominal diameter due to wear.",
    "wear_wires_localized": "Severe localized wear is visible on the outer wires.",
    "wear_wires_uniform": "There is excessive uniform wear throughout the rope.",
    "corrosion_wires_visible": "Visible severe external corrosion is present.",
    "corrosion_wires_signs": "There are signs of internal corrosion (diameter reduction, strand compression).",
    "corrosion_wires_cavities": "Corrosion with pitting (cavities) is present in the wires.",
    "deformation_wires_crushing": "There are crushing damages in the rope.",
    "deformation_wires_caging": "Bird caging deformation is observed.",
    "deformation_wires_protusion": "Core protrusion is visible.",
    "deformation_wires_knots": "There are kinks or knots in the rope.",
    "deformation_wires_flattening": "The rope shows excessive flattening.",
    "other_wires_heat": "There is damage caused by heat or high temperatures.",
    "other_wires_electrical": "Electrical damage is present (burn marks, wire fusion).",
    "other_wires_strands": "Wires or strands are displaced from their original position.",
    "other_wires_exposed": "The core of the rope is exposed.",
    "other_wires_terminal": "Terminals or connections show damage (cracks, deformations).",
    "lubrification_wires_lack": "There is a lack of adequate lubrication on the rope.",
    "lubrification_wires_drying": "Rope appears dry and has lost flexibility.",
    "conclusion_wires_suitable": "The element is suitable for use.",
    "lashing_wires_acceptance": "Wire rope or grommet has been inspected and the checklist has been completed according to the applicable standard."
}

POSITIVE_YES_FIELDS_WIRES = {
    "lashing_plan",
    "lashing_items",
    "lashing_material",
    "lashing_condition",
    "conclusion_wires_suitable",
    "lashing_wires_acceptance"
}

# Shackles
FIELD_DESCRIPTIONS_SHACKLES = {
    "lashing_plan": "Applied lashing arrangement is the same as the issued lashing plan.",
    "lashing_items": "lashing item certificates have been issued and verified. They are valid.",
    "lashing_material": "All lashing materials show visible capacity and are in accordance with the lashing plan.",
    "lashing_condition": "General condition of lashing materials is suitable for their intended purpose.",
    "visible_mark": "Manufacturer's mark or symbol is visible and legible.",
    "visible_grade_number": "Grade number (steel type) is visible and legible.",
    "visible_limit": "Working Load Limit (WLL/SWL) in tons is visible and legible.",
    "visible_pin_mark": "Manufacturer's mark is visible on pin (for pins ≥ 13 mm).",
    "visible_grade_material": "Material grade is visible and legible.",
    "compatible_pin": "Pin is compatible with the shackle body.",
    "fractures": "Are there cracks or fractures detected.",
    "deformations": "Are there deformations or elongations detected.",
    "corrosion": "Are there excessive corrosion present.",
    "wear": "Are there wear exceeding 10% of the section.",
    "notches": "Are there deep notches, cuts or grooves.",
    "overheating": "Are there signs of overheating or welding damage.",
    "bends": "Are there twists or bends observed.",
    "shackle_pin": "Pin fits correctly in the shackle body.",
    "tightened_pin": "Pin can be fully tightened.",
    "present_pin": "Nut and cotter pin are present and in good condition.",
    "lashing_shackles_acceptance": "Shackle has been inspected according to standard and checklist has been completed."
}

# Todos os campos são positivos se forem "Yes"
POSITIVE_YES_FIELDS_SHACKLES = {
    field for field, description in FIELD_DESCRIPTIONS_SHACKLES.items()
    if not description.startswith("Are there")
}

# --- Chain ---
FIELD_DESCRIPTIONS_CHAIN = {
    "lashing_plan": "Applied lashing arrangement is the same as the issued lashing plan.",
    "lashing_items": "lashing item certificates have been issued and verified. They are valid.",
    "lashing_material": "All lashing materials show visible capacity and are in accordance with the lashing plan.",
    "lashing_condition": "General condition of lashing materials is suitable for their intended purpose.",
    "visible_mark": "Manufacturer's mark or symbol is visible and legible.",
    "marked_grade": "Chain grade (e.g., 8, 10) is clearly marked.",
    "marked_limit": "Working Load Limit (WLL) is clearly marked.",
    "visible_traceability": "Serial number or traceability code is visible and legible.",
    "specified_length": "Chain length matches the specified length.",
    "sling_number": "Correct number of chain sling legs is present.",
    "legible_identification": "Identification tag is present and legible.",
    "marked_inspection": "Date of last inspection is marked and within validity.",
    "links_cracks": "There are cracks or breaks in the links.",
    "excessive_wear": "There are excessive wear, dents, or notches.",
    "links_stretched": "There are stretched or elongated links.",
    "links_twisted": "There are twisted, bent, or deformed links.",
    "corrosion": "There are excessive corrosion or pitting present.",
    "overheating": "There are evidence of overheating or welding damage.",
    "weld_splatter": "There are weld splatter adhered to the chain.",
    "links_obstructions": "Do all links move freely without obstructions.",
    "links_diameter": "Link diameter is within allowed tolerances.",
    "reduction_wear": "Are there diameter reductions greater than 10% due to wear.",
    "elongation_length": "Are there elongation greater than 5% of the original length.",
    "lashing_chain_acceptance": "Chain has been inspected according to the applicable standard. Checklist for chain has been filled."
}

POSITIVE_YES_FIELDS_CHAIN = {
    field for field, description in FIELD_DESCRIPTIONS_CHAIN.items()
    if not description.startswith("Are there")
}

# --- Synthetic Sling ---
FIELD_DESCRIPTIONS_SYNTHETIC_LINES = {
    "lashing_plan": "Applied lashing arrangement is the same as the issued lashing plan.",
    "lashing_items": "lashing item certificates have been issued and verified. They are valid.",
    "lashing_material": "All lashing materials show visible capacity and are in accordance with the lashing plan.",
    "lashing_condition": "General condition of lashing materials is suitable for their intended purpose.",
    "missing_label": "Are there the identification label missing or illegible.",
    "visible_capacity": "Are there the load capacity not clearly visible.",
    "core_exposure": "Are there core exposure (visible internal filaments).",
    "core_cut": "Are there cut filaments in the exposed core.",
    "core_broken": "Are there broken filaments in the exposed core.",
    "core_abrasion": "Are there excessive abrasion in the exposed core.",
    "damages_protection": "Are there the protective cover show significant damage.",
    "cut_any": "Are there any type of cut (longitudinal or transversal).",
    "cut_sides": "Are there cuts on the sides of the lines.",
    "punctures": "Are there punctures in the lines.",
    "abrasion": "Are there wear, fraying, or severe abrasion.",
    "damages_heat": "Are there damage from heat, weld splatter, or chemicals.",
    "excessive_friction": "Are there signs of heating or excessive friction (shiny or melted fibers).",
    "knots": "Are there the lines have knots or twists.",
    "modifications": "Are there unauthorized modifications to the lines.",
    "chemical_stains": "Are there the lines show chemical stains.",
    "overload": "Are there signs of previous overload (abnormal stretching).",
    "hardware_deformations": "Are there hardware (eyes, hooks, etc.) show deformations.",
    "wear_metal": "Are there excessive wear on the walls of metal parts.",
    "fractures": "Are there cracks or fractures in the hardware.",
    "hook_deformations": "Are there hook opening deformed (more than 10%).",
    "lashing_lines_acceptance": "Synthetic lines has been inspected according to the applicable standard. Checklist for synthetic lines has been filled."
}

POSITIVE_YES_FIELDS_SYNTHETIC_LINES = {
    field for field, description in FIELD_DESCRIPTIONS_SYNTHETIC_LINES.items()
    if not description.startswith("Are there")
}

# --- Synthetic Sling ---
FIELD_DESCRIPTIONS_TENSIONER = {
    "lashing_plan": "Applied lashing arrangement is the same as the issued lashing plan.",
    "lashing_items": "lashing item certificates have been issued and verified. They are valid.",
    "lashing_material": "All lashing materials show visible capacity and are in accordance with the lashing plan.",
    "lashing_condition": "General condition of lashing materials is suitable for their intended purpose.",
    "overheating": "There are evidence of overheating or welding damage.",
    "visible_mark": "Manufacturer's mark or symbol is visible and legible.",
    "legible_identification": "Identification tag is present and legible.",
    "marked_limit": "Working Load Limit (WLL) is clearly marked.",
    "visible_traceability": "Serial number or traceability code is visible and legible.",
    "cracks": "There are cracks or breaks in links.",
    "wear": "There are excessive wear, dents or notches.",
    "stretched": "There are stretched or elongated parts.",
    "twisted": "There are twisted, bent or deformed parts.",
    "corrosion": "There are excessive corrosion or pitting.",
    "lashing_tensioner_acceptance": "Tensioner has been inspected according with applied standard of acceptance. Check list for tensioner filled."
}

POSITIVE_YES_FIELDS_TENSIONER = {
    field for field, description in FIELD_DESCRIPTIONS_TENSIONER.items()
    if not description.startswith("Are there")
}

# --- Synthetic Sling ---
FIELD_DESCRIPTIONS_STOPPER = {
    "lashing_plan": "Applied lashing arrangement is the same as the issued lashing plan.",
    "lashing_items": "lashing item certificates have been issued and verified. They are valid.",
    "lashing_material": "All lashing materials show visible capacity and are in accordance with the lashing plan.",
    "lashing_condition": "General condition of lashing materials is suitable for their intended purpose.",
    "dimensions": "Dimensions of Stopper/dog plate are the same as indicated in lashing plan.",
    "wear": "There are excessive wear or dents.",
    "twisted": "There are twisted, bent or deformed body.",
    "corrosion": "There are excessive corrosion or pitting.",
    "lashing_stopper_acceptance": "Stopper,dog plate ,etc  has been inspected according with applied standard of acceptance. Check list for stopper/dog plate filled."
}

POSITIVE_YES_FIELDS_STOPPER = {
    field for field, description in FIELD_DESCRIPTIONS_STOPPER.items()
    if not description.startswith("Are there")
}

def ai_lashing_condition(data: dict[str, str], lashing_type: str) -> list[str]:
    """
    Gera até 6 observações técnicas em inglês para o tipo de levantamento informado (Wire Ropes ou Shackles),
    com base em campos considerados negativos.
    """
    # Configurações específicas por tipo
    if lashing_type == "Wire Ropes":
        descriptions = FIELD_DESCRIPTIONS_WIRE
        positives = POSITIVE_YES_FIELDS_WIRES
    elif lashing_type == "Shackles":
        descriptions = FIELD_DESCRIPTIONS_SHACKLES
        positives = POSITIVE_YES_FIELDS_SHACKLES
    elif lashing_type == "Tensioner, turnbuckle, arm lever":
        descriptions = FIELD_DESCRIPTIONS_TENSIONER
        positives = POSITIVE_YES_FIELDS_TENSIONER
    elif lashing_type == "Stopper, dog plate":
        descriptions = FIELD_DESCRIPTIONS_STOPPER
        positives = POSITIVE_YES_FIELDS_STOPPER
    elif lashing_type == "Chain":
        descriptions = FIELD_DESCRIPTIONS_CHAIN
        positives = POSITIVE_YES_FIELDS_CHAIN
    elif lashing_type == "Synthetic Lines":
        descriptions = FIELD_DESCRIPTIONS_SYNTHETIC_LINES
        positives = POSITIVE_YES_FIELDS_SYNTHETIC_LINES
    else:
        return ["Unsupported lashing type."]

    filtered_descriptions = {}

    for key, value in data.items():
        description = descriptions.get(key, key)

        if key in positives:
            if value != "Yes" and value != "Does Not Apply":
                filtered_descriptions[description] = value  # considerado negativo
        else:
            if value == "Yes":
                filtered_descriptions[description] = value  # considerado negativo

    if not filtered_descriptions:
        return ["No negative findings observed."]

    try:
        raw_content = prompt_model(
            system=(
                f"You are a technical inspector specialized in lashing gear inspections ({lashing_type}). "
                "The user is giving you only the fields that failed the inspection — do not assume or infer anything else. "
                "Generate up to SIX concise and professional technical remarks ONLY about those problems. "
                "DO NOT generate any comment about components that are OK or have no issues. "
                "DO NOT assume a field means 'OK' just because the description mentions 'no cracks' or 'no wear' — the input is filtered to only show problems. "
                "Avoid repeating comments about the same issue. If a single issue is detected (e.g. a cut), write only one observation about it. "
                "Write each remark like a real inspection report. "
                "Each sentence must be in English, under 90 words, start with uppercase, and end with a period. "
                "Return only a JSON array of 1 to 6 strings — no explanations or formatting."
            ),
            user=json.dumps(filtered_descriptions),
            max_tokens=1200,
        )

        clean = re.sub(r"```(?:json|text)?", "", raw_content).strip()
        obs_bullets = json.loads(clean)

        if not (isinstance(obs_bullets, list) and 1 <= len(obs_bullets) <= 6 and all(isinstance(s, str) for s in obs_bullets)):
            raise ValueError("Unexpected format returned by model.")

        return obs_bullets

    except (ValueError, json.JSONDecodeError) as exc:
        logging.warning(f"Failed to generate lashing inspection comments: {exc}")
        return ["Overall, the lashing material was determined to be in satisfactory operational condition."]
    except Exception as exc:
        logging.warning(f"Failed to generate lashing inspection comments: {exc}")
        return ["Overall, the lashing material was determined to be in satisfactory operational condition."]
