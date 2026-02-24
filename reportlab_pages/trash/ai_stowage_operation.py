import json
import os
import logging
import re
from openai import OpenAI, OpenAIError     # pip install openai>=1.0.0  (ou v0.x se estiver usando o client antigo)
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Pega a chave da variável de ambiente
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def generate_general_stowage_comment(variations: list[dict[str, str]], cod_atividade) -> list[str]:
    stowage_questions = {
        "proper_stowage": "Cargo has been properly stowage as per stowage plan ?",
        "obstructions_stowage": "Cargo has been stowage on flat surface without obstructions which may cause risks during navigation?",
        "proper_plating": "Wooden or/and Rubber have been properly placed between cargo and vessel plating ?",
        "surrounded_risks": "Cargo is free of iminent risks from surrouned cargos from another clients/shipments ?",
        "damages_internal": "Are there any hot works close to the cargo that may cause damage to internal circuits or similar?",
        "contaminant": "Are there any contaminants found near the cargo stowage area?"
    }

    observations = []
    if cod_atividade == "2":
        tipo = "storage"
    else:
        tipo = "stowage"

    for var in variations:
        # Filtra respostas relevantes
        respostas_legiveis = {
            stowage_questions[key]: val
            for key, val in var.items()
            if val and val != "Does Not Apply" and key in stowage_questions
        }

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.4,
                max_tokens=1200,
                top_p=1,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are a marine cargo surveyor. You are analyzing multiple {tipo} inspection records, each represented by a set of answers. "
                            f"Each set refers to a different cargo {tipo} situation on a vessel. Your task is to write ONE general, professional, and concise observation, "
                            f"in English, that summarizes the overall quality, risks, and findings of all {tipo} operations combined. "
                            f"Highlight recurring issues such as poor {tipo} practices, contamination, improper use of dunnage or plating, obstructions, or surrounding risks. "
                            f"If any good practices or well-executed {tipo} conditions are observed, mention them briefly. "
                            "Write a single paragraph of up to 500 words. "
                            "Respond only with a JSON array of 1 string, no introduction or explanation."
                        )
                    },
                    {
                        "role": "user",
                        "content": json.dumps(respostas_legiveis)
                    }
                ]
            )

            raw_content = response.choices[0].message.content
            clean = re.sub(r"```(\w+)?", "", raw_content).strip()
            obs = json.loads(clean)[0]
            observations.append(obs)

        except (OpenAIError, ValueError, json.JSONDecodeError) as exc:
            logging.warning(f"Failed to generate stowage comment for one variation: {exc}")
            observations.append("No further comments to be made.")

    return observations