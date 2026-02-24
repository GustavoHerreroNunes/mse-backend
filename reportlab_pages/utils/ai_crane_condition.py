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

def ai_crane_condition(data: dict[str, str]) -> list[str]:
    """
    data = {
        "external_cranes": "Fair",
        "wire": "Good",
        "sheaves": "Fair",
        "operation_condition": "Very Good"
    }
    Retorna uma lista com 3 sentenças (máx. 50 palavras cada) descrevendo genericamente
    o estado do guindaste com base nas 4 condições.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=250,           # 3 bullets x ~50 words ≃ 180 tokens + margem
            top_p=1,
            # A saída DEVE ser JSON minimamente válido para parse automático.
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a marine crane surveyor. "
                        "Generate exactly three concise, professional PLUS-point observations (ENG) "
                        "based on the 4 condition fields provided by the user. "
                        "Each sentence must be **max 50 words**, start with an uppercase letter, "
                        "and end with a period. "
                        "Respond **only** with a JSON array of 3 strings, nothing else."
                    )
                },
                {
                    "role": "user",
                    "content": json.dumps(data)
                }
            ]
        )
        raw_content = response.choices[0].message.content
        # remove ```json, ```text, ``` ou ```
        clean = re.sub(r"```(\w+)?", "", raw_content).strip()
        obs_bullets = json.loads(clean)
        # Garantir lista de str e tamanho correto
        if not (isinstance(obs_bullets, list) and len(obs_bullets) == 3 and all(isinstance(s, str) for s in obs_bullets)):
            raise ValueError("Formato inesperado retornado pelo modelo.")
        return obs_bullets

    except (OpenAIError, ValueError, json.JSONDecodeError) as exc:
        # Fallback seguro: usa mensagens default ou relança erro conforme sua política
        logging.warning(f"Falha ao gerar comentários automáticos: {exc}")
        return [
            "No further comments to be made."
        ]