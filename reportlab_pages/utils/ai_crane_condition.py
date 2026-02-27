import json
import logging
import re
from reportlab_pages.utils.gemini_client import prompt_model


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
        raw_content = prompt_model(
            system=(
                "You are a marine crane surveyor. "
                "Generate exactly three concise, professional PLUS-point observations (ENG) "
                "based on the 4 condition fields provided by the user. "
                "Each sentence must be **max 50 words**, start with an uppercase letter, "
                "and end with a period. "
                "Respond **only** with a JSON array of 3 strings, nothing else."
            ),
            user=json.dumps(data),
            max_tokens=250,
        )
        # remove ```json, ```text, ``` ou ```
        clean = re.sub(r"```(\w+)?", "", raw_content).strip()
        obs_bullets = json.loads(clean)
        # Garantir lista de str e tamanho correto
        if not (isinstance(obs_bullets, list) and len(obs_bullets) == 3 and all(isinstance(s, str) for s in obs_bullets)):
            raise ValueError("Formato inesperado retornado pelo modelo.")
        return obs_bullets

    except (ValueError, json.JSONDecodeError) as exc:
        logging.warning(f"Falha ao gerar comentários automáticos: {exc}")
        return [
            "No further comments to be made."
        ]
    except Exception as exc:
        logging.warning(f"Falha ao gerar comentários automáticos: {exc}")
        return [
            "No further comments to be made."
        ]
