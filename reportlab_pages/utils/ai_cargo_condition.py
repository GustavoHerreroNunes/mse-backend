import json
import logging
import re
from reportlab_pages.utils.gemini_client import prompt_model


def ai_cargo_condition(data: dict[str, str]) -> list[str]:
    """
    Gera até 6 observações técnicas em inglês para cargas tipo Wooden Crate, baseadas em
    condições negativas. Frases devem parecer saídas de um laudo técnico real.
    """
    try:
        raw_content = prompt_model(
            system=(
                "You are a cargo surveyor writing professional English remarks for a condition report on a cargo crate. "
                "Analyze the cargo condition fields provided and generate UP TO SIX bullet-point style technical observations, "
                "ONLY if there are negative findings (Fair, Poor, Very Poor, No, Minor, Moderate, Severe). "
                "And never ignore negative finding, always commenting about them. "
                "IMPORTANT: For 'moisture' and 'shifting', value 'No' is POSITIVE and should NOT be flagged. "
                "Each comment should be written naturally, e.g., 'Scratches noted on exposed wood surfaces.', not 'ranking_scratches: Moderate'. "
                "Each sentence must be concise, under 70 words, start with uppercase, and end with a period. "
                "Return only a JSON array of 1 to 6 English strings — no explanations, no code blocks."
            ),
            user=json.dumps(data),
            max_tokens=900,
        )
        clean = re.sub(r"```(?:json|text)?", "", raw_content).strip()
        obs_bullets = json.loads(clean)

        if not (isinstance(obs_bullets, list) and 1 <= len(obs_bullets) <= 6 and all(isinstance(s, str) for s in obs_bullets)):
            raise ValueError("Formato inesperado retornado pelo modelo.")

        return obs_bullets

    except (ValueError, json.JSONDecodeError) as exc:
        logging.warning(f"Falha ao gerar comentários automáticos: {exc}")
        return [
            "No further comments to be made.",
        ]
    except Exception as exc:
        logging.warning(f"Falha ao gerar comentários automáticos: {exc}")
        return [
            "No further comments to be made.",
        ]
