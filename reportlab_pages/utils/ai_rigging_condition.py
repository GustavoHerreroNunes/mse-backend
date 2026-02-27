import json
import logging
import re
from reportlab_pages.utils.gemini_client import prompt_model

# --- Synthetic Sling ---
FIELD_DESCRIPTIONS = {
    "elements_accordance": "Applied rigging elements in accordance with the issued lifting plan",
    "elements_fitted": "Rigging elements were well fitted to cargo lifting points",
    "safety_devices": "Safety devices or pins (shackles, hooks, etc.) were applied",
    "twisted_line": "Are there any twisted lifting line",
    "slings_contact": "Are there any contact of slings with sharp edges or similar hazards",
    "beginning_inclination": "Cargo was steady at the beginning of lifting with no tilt/inclination",
    "during_inclination": "Are there abnormal or excessive vessel inclination occurred during lifting",
    "has_pictures_elements": "Pictures of the rigging elements connected were taken",
    "has_pictures_beginning": "Pictures of the beginning of the lifting operation were taken",
    "has_pictures_overall": "Pictures of the overall lifting operation were taken",
    "has_pictures_stowage": "Pictures of the stowage of the cargo after lifting were taken"
}

POSITIVE_YES_FIELDS = {
    field for field, description in FIELD_DESCRIPTIONS.items()
    if not description.startswith("Are there")
}

def ai_rigging_condition(data: dict[str, str]) -> list[str]:
    """
    Gera até 6 observações técnicas em inglês para o tipo de levantamento informado (Wire Ropes ou Shackles),
    com base em campos considerados negativos.
    """
    # Configurações específicas por tipo
    descriptions = FIELD_DESCRIPTIONS
    positives = POSITIVE_YES_FIELDS

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
                "You are a technical inspector specialized in lifting operations of a cargo. "
                "The user is providing you with only the inspection items that FAILED during a cargo lifting operation — these are operational or safety issues that occurred. "
                "Generate up to SIX concise and professional technical remarks about these issues. "
                "DO NOT generate comments about elements that passed or are not mentioned. "
                "Avoid redundancy: if multiple fields refer to the same issue (e.g., slings twisted or poorly positioned), summarize into a single comment. "
                "Write each observation like an official inspection report note, in clear technical English. "
                "Each sentence must be under 90 words, start with uppercase, and end with a period. "
                "Return ONLY a JSON array of 1 to 6 strings — no explanations, markdown, or formatting outside the array."
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
        return ["No further comments to be made."]
    except Exception as exc:
        logging.warning(f"Failed to generate lifting inspection comments: {exc}")
        return ["No further comments to be made."]
