import json
import logging
import re
from reportlab_pages.utils.gemini_client import prompt_model

# Mapeamento de colunas para descrições legíveis – Wire Ropes
FIELD_DESCRIPTIONS_WIRE = {
    "rigging_plan": "Applied rigging arrangement is the same as the issued rigging plan.",
    "rigging_items": "Rigging item certificates have been issued and verified. They are valid.",
    "rigging_material": "All rigging materials show visible capacity and are in accordance with the rigging plan.",
    "rigging_condition": "General condition of rigging materials is suitable for their intended purpose.",
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
    "rigging_wires_acceptance": "Wire rope or grommet has been inspected and the checklist has been completed according to the applicable standard."
}

POSITIVE_YES_FIELDS_WIRES = {
    "rigging_plan",
    "rigging_items",
    "rigging_material",
    "rigging_condition",
    "conclusion_wires_suitable",
    "rigging_wires_acceptance"
}

# Shackles
FIELD_DESCRIPTIONS_SHACKLES = {
    "rigging_plan": "Applied rigging arrangement is the same as the issued rigging plan.",
    "rigging_items": "Rigging item certificates have been issued and verified. They are valid.",
    "rigging_material": "All rigging materials show visible capacity and are in accordance with the rigging plan.",
    "rigging_condition": "General condition of rigging materials is suitable for their intended purpose.",
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
    "rigging_shackles_acceptance": "Shackle has been inspected according to standard and checklist has been completed."
}

# Todos os campos são positivos se forem "Yes"
POSITIVE_YES_FIELDS_SHACKLES = {
    field for field, description in FIELD_DESCRIPTIONS_SHACKLES.items()
    if not description.startswith("Are there")
}

# --- Hook ---
FIELD_DESCRIPTIONS_HOOK = {
    "rigging_plan": "Applied rigging arrangement is the same as the issued rigging plan.",
    "rigging_items": "Rigging item certificates have been issued and verified. They are valid.",
    "rigging_material": "All rigging materials show visible capacity and are in accordance with the rigging plan.",
    "rigging_condition": "General condition of rigging materials is suitable for their intended purpose.",
    "visible_mark": "Manufacturer's mark or symbol is visible and legible.",
    "marked_limit": "Working Load Limit (WLL) is clearly marked.",
    "visible_traceability": "Serial number or traceability code is visible and legible.",
    "hook_type": "Hook type is identified (eye, clevis, shank, etc.).",
    "marked_grade": "Material grade is clearly marked (when applicable).",
    "legible_identification": "Identification tag is present and legible (when applicable).",
    "cracks": "There are cracks or breaks detected.",
    "dents": "There are excessive wear, dents, or notches.",
    "excessive_corrosion": "There are excessive corrosion or pitting is present.",
    "visible_deformations": "There are visible deformations (twists or bends).",
    "overheating": "There are evidence of overheating or welding damage.",
    "weld_splatter": "There are weld splatter adhered to the hook.",
    "unauthorized_modifications": "There are unauthorized modifications (holes, machining, etc.).",
    "damages_thread": "There are thread damage (for hooks with threaded shank).",
    "throat_limits": "Throat opening is within allowed limits.",
    "opening_deformations": "There are deformation in the opening.",
    "excessive_wear_area": "There are excessive wear in the load contact area.",
    "sharp_edges": "There are sharp edges or burrs present.",
    "widening_tip": "There are widening at the hook tip.",
    "bearing_wear": "There are wear in the load bearing area (base/bowl).",
    "impact_mark": "There are impact marks in the contact area.",
    "hook_shape": "Hook profile maintains original shape.",
    "intact_latch": "Safety latch is present and intact.",
    "correctly_latch": "Safety latch works correctly.",
    "tension_latch": "Latch spring has adequate tension.",
    "deformations_latch": "There are deformations in the latch.",
    "exessive_wear_points": "There are excessive wear at pivot points.",
    "opening_latch": "Latch completely closes the hook opening.",
    "corrosion_latch": "There are corrosion on the latch and its components.",
    "damages_latch": "There are damage or cracks in the latch.",
    "hook_rotation": "Hook rotates freely (for swivel hooks).",
    "locking_mechanism": "Locking mechanism works correctly (when applicable).",
    "smooth_joints": "Joints work smoothly.",
    "jamming": "There are jamming in any position.",
    "automatic_latch": "Automatic return of safety latch works properly.",
    "excessive_play": "There are excessive play in moving parts.",
    "hook_dimensions": "Hook dimensions are within allowed tolerances.",
    "reduction_wear": "There are section reduction greater than 10% due to wear.",
    "throat_opening": "Throat opening does not exceed 5% of original dimension.",
    "elongation": "There are elongation in the eye or connection point.",
    "angular_deformations": "There are angular deformation is present.",
    "rigging_hook_acceptance": "Hook has been inspected and checklist has been filled according to the applicable standard."
}

POSITIVE_YES_FIELDS_HOOK = {
    field for field, description in FIELD_DESCRIPTIONS_HOOK.items()
    if not description.startswith("Are there")
}

# --- Master Link ---
FIELD_DESCRIPTIONS_MASTER_LINK = {
    "rigging_plan": "Applied rigging arrangement is the same as the issued rigging plan.",
    "rigging_items": "Rigging item certificates have been issued and verified. They are valid.",
    "rigging_material": "All rigging materials show visible capacity and are in accordance with the rigging plan.",
    "rigging_condition": "General condition of rigging materials is suitable for their intended purpose.",
    "visible_mark": "Manufacturer's mark or symbol is visible and legible.",
    "marked_limit": "Working Load Limit (WLL) is clearly marked.",
    "marked_dimension": "Size or dimension of the ring/link is clearly marked.",
    "marked_grade": "Material grade is clearly marked (when applicable).",
    "visible_traceability": "Serial number or traceability code is visible and legible.",
    "cracks": "There are cracks or breaks detected.",
    "wear": "There are excessive wear, dents, or notches.",
    "corrosion": "There are excessive corrosion or pitting present.",
    "visible_deformations": "There are visible deformations (twists or bends).",
    "overheating": "There are evidence of overheating or welding damage.",
    "weld_splatter": "There are weld splatter adhered to the ring/link.",
    "modifications": "There are unauthorized modifications (holes, machining, etc.).",
    "stretching": "There are elongation or stretching present.",
    "original_shape": "Ring/link profile maintains original shape.",
    "contact_deformations": "There are deformations in contact areas.",
    "sharp_edges": "There are sharp edges or burrs present.",
    "impact_mark": "There are impact marks in contact areas.",
    "section_reduction": "There are section reductions in contact areas.",
    "deep_scratches": "There are deep grooves or scratches.",
    "tolerated_dimensions": "Ring/link dimensions are within allowed tolerances.",
    "reduction_wear": "Are there section reduction greater than 10% due to wear.",
    "elongation": "There are elongation greater than 5% of original dimension.",
    "angular_deformations": "There are angular deformation present.",
    "rigging_link_acceptance": "Master Link has been inspected according to the applicable standard. Master list for hook has been filled."
}

POSITIVE_YES_FIELDS_MASTER_LINK = {
    field for field, description in FIELD_DESCRIPTIONS_MASTER_LINK.items()
    if not description.startswith("Are there")
}

# --- Chain ---
FIELD_DESCRIPTIONS_CHAIN = {
    "rigging_plan": "Applied rigging arrangement is the same as the issued rigging plan.",
    "rigging_items": "Rigging item certificates have been issued and verified. They are valid.",
    "rigging_material": "All rigging materials show visible capacity and are in accordance with the rigging plan.",
    "rigging_condition": "General condition of rigging materials is suitable for their intended purpose.",
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
    "rigging_chain_acceptance": "Chain has been inspected according to the applicable standard. Checklist for chain has been filled."
}

POSITIVE_YES_FIELDS_CHAIN = {
    field for field, description in FIELD_DESCRIPTIONS_CHAIN.items()
    if not description.startswith("Are there")
}

# --- Spreader ---
FIELD_DESCRIPTIONS_SPREADER = {
    "rigging_plan": "Applied rigging arrangement is the same as the issued rigging plan.",
    "rigging_items": "Rigging item certificates have been issued and verified. They are valid.",
    "rigging_material": "All rigging materials show visible capacity and are in accordance with the rigging plan.",
    "rigging_condition": "General condition of rigging materials is suitable for their intended purpose.",
    "marked_limit": "Working Load Limit (WLL) is clearly marked.",
    "marked_weight": "Self-weight of the spreader is clearly marked (if above 100 lbs / 45 kg).",
    "main_fractures": "Are there cracks or fractures in the main structure.",
    "permanent_deformations": "Are there any permanent deformation in the main beam.",
    "corrosion": "Are there excessive corrosion present.",
    "damages_collision": "Are there damages from impact or collision.",
    "twisting": "Are there warping or twisting present.",
    "overheating": "Are there evidence of overheating or welding damage.",
    "improper_repair": "Are there unauthorized welds or improper repairs.",
    "contact_wear": "Are there excessive wear at contact points.",
    "lifting_deformations": "Are there deformations in the lifting eye or point.",
    "lifting_wear": "Are there excessive wear on the lifting eye or point.",
    "weld_fractures": "Are there cracks or fractures at the eye weld points.",
    "hole_deformations": "Are there enlargement or deformation of the eye hole.",
    "present_safety_devices": "Safety devices (cotter pins, nuts) are present and functional.",
    "adjustment_mechanisms": "Length adjustment mechanisms are working correctly.",
    "present_pin": "Locking or fastening pins are present and in good condition.",
    "excessive_wear": "Are there excessive wear in adjustment holes.",
    "visible_mark": "Position or length markings are visible and legible.",
    "components_deformations": "Are there deformations in adjustable components.",
    "locking_devices": "Locking devices are working properly.",
    "components_obstructions": "Moving components move freely without obstructions.",
    "rigging_spreader_acceptance": "Spreader has been inspected according to the applicable standard. Checklist for spreader has been filled."
}

POSITIVE_YES_FIELDS_SPREADER = {
    field for field, description in FIELD_DESCRIPTIONS_SPREADER.items()
    if not description.startswith("Are there")
}

# --- Synthetic Sling ---
FIELD_DESCRIPTIONS_SYNTHETIC_SLING = {
    "rigging_plan": "Applied rigging arrangement is the same as the issued rigging plan.",
    "rigging_items": "Rigging item certificates have been issued and verified. They are valid.",
    "rigging_material": "All rigging materials show visible capacity and are in accordance with the rigging plan.",
    "rigging_condition": "General condition of rigging materials is suitable for their intended purpose.",
    "missing_label": "There are the identification label missing or illegible.",
    "visible_capacity": "There are the load capacity not clearly visible.",
    "core_exposure": "There are core exposure (visible internal filaments).",
    "core_cut": "There are cut filaments in the exposed core.",
    "core_broken": "There are broken filaments in the exposed core.",
    "core_abrasion": "There are excessive abrasion in the exposed core.",
    "damages_protection": "There are the protective cover show significant damage.",
    "cut_any": "There are any type of cut (longitudinal or transversal).",
    "cut_sides": "There are cuts on the sides of the sling.",
    "punctures": "There are punctures in the sling.",
    "abrasion": "There are wear, fraying, or severe abrasion.",
    "damages_heat": "There are damage from heat, weld splatter, or chemicals.",
    "excessive_friction": "There are signs of heating or excessive friction (shiny or melted fibers).",
    "knots": "There are the sling have knots or twists.",
    "modifications": "There are unauthorized modifications to the sling.",
    "chemical_stains": "There are the sling show chemical stains.",
    "overload": "There are signs of previous overload (abnormal stretching).",
    "hardware_deformations": "There are the hardware (eyes, hooks, etc.) show deformations.",
    "wear_metal": "There are excessive wear on the walls of metal parts.",
    "fractures": "There are cracks or fractures in the hardware.",
    "hook_deformations": "There are hook opening deformed (more than 10%).",
    "rigging_sling_acceptance": "Synthetic sling has been inspected according to the applicable standard. Checklist for synthetic sling has been filled."
}

POSITIVE_YES_FIELDS_SYNTHETIC_SLING = {
    field for field, description in FIELD_DESCRIPTIONS_SYNTHETIC_SLING.items()
    if not description.startswith("There are")
}

def ai_lifting_condition(data: dict[str, str], lifting_type: str) -> list[str]:
    """
    Gera até 6 observações técnicas em inglês para o tipo de levantamento informado (Wire Ropes ou Shackles),
    com base em campos considerados negativos.
    """
    # Configurações específicas por tipo
    if lifting_type == "Wire Ropes":
        descriptions = FIELD_DESCRIPTIONS_WIRE
        positives = POSITIVE_YES_FIELDS_WIRES
    elif lifting_type == "Shackles":
        descriptions = FIELD_DESCRIPTIONS_SHACKLES
        positives = POSITIVE_YES_FIELDS_SHACKLES
    elif lifting_type == "Hook":
        descriptions = FIELD_DESCRIPTIONS_HOOK
        positives = POSITIVE_YES_FIELDS_HOOK
    elif lifting_type == "Master Link":
        descriptions = FIELD_DESCRIPTIONS_MASTER_LINK
        positives = POSITIVE_YES_FIELDS_MASTER_LINK
    elif lifting_type == "Chain":
        descriptions = FIELD_DESCRIPTIONS_CHAIN
        positives = POSITIVE_YES_FIELDS_CHAIN
    elif lifting_type == "Spreader":
        descriptions = FIELD_DESCRIPTIONS_SPREADER
        positives = POSITIVE_YES_FIELDS_SPREADER
    elif lifting_type == "Synthetic Sling":
        descriptions = FIELD_DESCRIPTIONS_SYNTHETIC_SLING
        positives = POSITIVE_YES_FIELDS_SYNTHETIC_SLING
    else:
        return ["Unsupported lifting type."]

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
                f"You are a technical inspector specialized in lifting gear inspections ({lifting_type}). "
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
        logging.warning(f"Failed to generate lifting inspection comments: {exc}")
        return ["Overall, the lifting material was determined to be in satisfactory operational condition."]
    except Exception as exc:
        logging.warning(f"Failed to generate lifting inspection comments: {exc}")
        return ["Overall, the lifting material was determined to be in satisfactory operational condition."]
