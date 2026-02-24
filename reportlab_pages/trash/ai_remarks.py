from collections import defaultdict
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

def ai_remarks(all_comments: list[list[dict]]) -> list[dict]:
    final_remarks = []

    # Agrupar comentários por seção
    grouped_comments = defaultdict(list)

    for section_group in all_comments:
        for item in section_group:
            section = item.get("section", "Unknown Section")
            comments = item.get("comments", [])

            # Caso o campo comments seja string em vez de lista, converte
            if isinstance(comments, str):
                comments = [comments]

            grouped_comments[section].extend(comments)

    for section, comments in grouped_comments.items():
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.4,
                max_tokens=500,
                top_p=1,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a QHSE (Quality, Health, Safety, and Environment) marine surveyor. "
                            "Based on the provided inspection comments, generate up to five concise, professional remarks "
                            "highlighting the most important points to improve and any relevant observations. "
                            "Each remark must be in English, under 50 words, and end with a period. "
                            "Respond only with a JSON array of 1 to 5 strings, no title or introduction."
                        )
                    },
                    {
                        "role": "user",
                        "content": json.dumps(comments)
                    }
                ]
            )

            raw_content = response.choices[0].message.content
            clean = re.sub(r"```(\w+)?", "", raw_content).strip()
            remarks = json.loads(clean)

            if not (isinstance(remarks, list) and 1 <= len(remarks) <= 5 and all(isinstance(s, str) for s in remarks)):
                raise ValueError("Formato inesperado retornado pelo modelo.")

            final_remarks.append({
                "section": section,
                "remarks": remarks
            })

        except (OpenAIError, ValueError, json.JSONDecodeError) as exc:
            logging.warning(f"Falha ao gerar comentários para {section}: {exc}")
            final_remarks.append({
                "section": section,
                "remarks": ["No further comments to be made."]
            })

    return final_remarks
