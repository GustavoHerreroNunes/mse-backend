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

def ai_cargo_condition(data: dict[str, str]) -> list[str]:
    """
    Gera até 6 observações técnicas em inglês para cargas tipo Wooden Crate, baseadas em
    condições negativas. Frases devem parecer saídas de um laudo técnico real.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=900,
            top_p=1,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a cargo surveyor writing professional English remarks for a condition report on a cargo crate. "
                        "Analyze the cargo condition fields provided and generate UP TO SIX bullet-point style technical observations, "
                        "ONLY if there are negative findings (Fair, Poor, Very Poor, No, Minor, Moderate, Severe). "
                        "And never ignore negative finding, always commenting about them. "
                        "IMPORTANT: For 'moisture' and 'shifting', value 'No' is POSITIVE and should NOT be flagged. "
                        "Each comment should be written naturally, e.g., 'Scratches noted on exposed wood surfaces.', not 'ranking_scratches: Moderate'. "
                        "Each sentence must be concise, under 70 words, start with uppercase, and end with a period. "
                        "Return only a JSON array of 1 to 6 English strings — no explanations, no code blocks."
                    )
                },
                {
                    "role": "user",
                    "content": json.dumps(data)
                }
            ]
        )
        raw_content = response.choices[0].message.content
        clean = re.sub(r"```(?:json|text)?", "", raw_content).strip()
        obs_bullets = json.loads(clean)

        if not (isinstance(obs_bullets, list) and 1 <= len(obs_bullets) <= 6 and all(isinstance(s, str) for s in obs_bullets)):
            raise ValueError("Formato inesperado retornado pelo modelo.")

        return obs_bullets

    except (OpenAIError, ValueError, json.JSONDecodeError) as exc:
        logging.warning(f"Falha ao gerar comentários automáticos: {exc}")
        return [
            "No further comments to be made.",
        ]