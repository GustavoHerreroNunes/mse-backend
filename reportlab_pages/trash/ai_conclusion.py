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

def ai_conclusion(all_comments: list[list[dict]]) -> list[dict]:
    final_remarks = []

    # Agrupar comentários por seção
    grouped_comments = defaultdict(list)

    for section_group in all_comments:
        for item in section_group:
            section = item.get("section", "Unknown Section")
            comments = item.get("comments", [])

            if isinstance(comments, str):
                comments = [comments]

            grouped_comments[section].extend(comments)

    for section, comments in grouped_comments.items():
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.4,
                max_tokens=250,
                top_p=1,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a QHSE (Quality, Health, Safety, and Environment) marine surveyor. "
                            "Based on the provided inspection comments, write a single professional summary remark for the section "
                            f"titled '{section}', under the topic 'CONCLUSION/REMARKS'. "
                            "The remark should summarize the overall condition, highlight major concerns, and suggest any needed improvements. "
                            "It must be in English, professional, under 70 words, and end with a period. "
                            "Respond only with a JSON string (i.e., a quoted sentence), no array or title."
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
            remark = json.loads(clean)

            if not isinstance(remark, str):
                raise ValueError("Formato inesperado retornado pelo modelo.")

            final_remarks.append({
                "section": section,
                "remark": remark
            })

        except (OpenAIError, ValueError, json.JSONDecodeError) as exc:
            logging.warning(f"Falha ao gerar conclusão para {section}: {exc}")
            final_remarks.append({
                "section": section,
                "remark": "No conclusion available for this section."
            })

    return final_remarks
