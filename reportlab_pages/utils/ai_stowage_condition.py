import json
import os
import logging
import re
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# --- Synthetic Sling ---
FIELD_DESCRIPTIONS = {
    "proper_stowage": "Cargo has been properly stowed as per stowage plan",
    "obstructions_stowage": "Cargo has been stowed on a flat surface without obstructions that may cause risks during navigation",
    "proper_plating": "Wooden and/or rubber dunnage has been properly placed between cargo and vessel plating",
    "surrounded_risks": "Cargo is free of imminent risks from surrounding cargo belonging to other clients/shipments",
    "damages_internal": "Hot works close to the cargo may cause damage to internal circuits or similar hazards",
    "contaminant": "There are contaminants found near the cargo stowage area"
}

# Campos onde "Yes" é positivo (boas práticas); em todos os outros, "Yes" indica problema
POSITIVE_YES_FIELDS = {
    field for field, description in FIELD_DESCRIPTIONS.items()
    if not description.startswith("Hot works") and not description.startswith("There are")
}

def ai_stowage_condition(data: dict[str, str], tipo: str) -> list[str]:
    """
    Gera até 6 observações técnicas em inglês para o tipo de levantamento informado,
    com base em campos considerados negativos.
    """
    descriptions = FIELD_DESCRIPTIONS
    positives = POSITIVE_YES_FIELDS

    filtered_descriptions = {}

    for key, value in data.items():
        description = descriptions.get(key, key)

        if key in positives:
            # Exemplo: "proper_stowage" esperado = Yes, mas se veio "No", é problema
            if value not in ("Yes", "Does Not Apply"):
                filtered_descriptions[description] = value
        else:
            # Exemplo: "damages_internal" esperado = No, mas se veio "Yes", é problema
            if value == "Yes":
                filtered_descriptions[description] = value

    if not filtered_descriptions:
        return ["No negative findings observed."]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=800,
            top_p=1,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a marine cargo surveyor specialized in {tipo}. "
                        "The user provides you only with FAILED inspection items — these represent safety or operational risks. "
                        "Generate up to SIX concise and professional technical remarks about these issues. "
                        "DO NOT generate comments about items that passed or are not provided. "
                        "Avoid redundancy: if multiple fields refer to the same issue, summarize into a single comment. "
                        "Each sentence must be clear technical English, under 90 words, starting with uppercase and ending with a period. "
                        "Return ONLY a JSON array of 1 to 6 strings — no explanations, markdown, or formatting outside the array."
                    )
                },
                {
                    "role": "user",
                    "content": json.dumps(filtered_descriptions)
                }
            ]
        )

        raw_content = response.choices[0].message.content
        clean = re.sub(r"```(?:json|text)?", "", raw_content).strip()
        obs_bullets = json.loads(clean)

        if not (isinstance(obs_bullets, list) and 1 <= len(obs_bullets) <= 6 and all(isinstance(s, str) for s in obs_bullets)):
            raise ValueError("Unexpected format returned by model.")

        return obs_bullets

    except (OpenAIError, ValueError, json.JSONDecodeError) as exc:
        logging.warning(f"Failed to generate {tipo} inspection comments: {exc}")
        return ["No further comments to be made."]
