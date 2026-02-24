from .utils.draw_commons_images import draw_separator_image, draw_header, draw_footer
from .utils.draw_wrapped_text import draw_wrapped_text
from .utils.draw_page_number import draw_page_number
from querys.get_dados_conclusion_cargo import get_dados_ia_conclusion_cargo
from querys.get_dados_conclusion_lashing import get_dados_ia_conclusion_lashing
from querys.get_dados_conclusion_lifting import get_dados_ia_conclusion_lifting
from querys.get_dados_conclusion_rigging import get_dados_ia_conclusion_rigging

def draw_conclusion_page(c, width, height, cod_atividade, demanda_id):
    draw_header(c, width, height)
    draw_footer(c, width)
    draw_page_number(c, width)

    if cod_atividade == "2":
        title = "11. CONCLUSION/ REMARKS"
    else:
        title = "12. CONCLUSION/ REMARKS"

    title_font = "CooperBlack"
    title_size = 20
    title_y = height - 150
    c.setFont(title_font, title_size)
    c.drawString(30, title_y, title)

    margin_x = 30
    max_width = width - (margin_x * 2)
    font_size = 13
    leading = 14
    current_y = title_y - 40

    def draw_paragraph(text, y, font_name, x=30):
        lines = draw_wrapped_text(
            c, text, x, y, max_width - (x - 30), font_name, font_size, leading
        )
        return lines[-1][2] - leading if lines else y - leading

    # Chamadas para cada get_conclusion
    cargo_condition, _ = get_dados_ia_conclusion_cargo(demanda_id)
    lifting_condition, _ = get_dados_ia_conclusion_lifting(demanda_id)
    lashing_condition, _ = get_dados_ia_conclusion_lashing(demanda_id)
    rigging_condition, _ = get_dados_ia_conclusion_rigging(demanda_id)

    # Dicionário de textos
    condition_texts = {
        "cargo_condition": {
            "Good": "The cargo has been inspected and found in good condition, with no visible damage or abnormalities.",
            "Bad": "Cargo shows signs of damage or irregularities and does not meet standard condition requirements."
        },
        "lifting_condition": {
            "Good": "All lifting items have been inspected and are in good working condition, with no visible defects.",
            "Bad": "One or more lifting items have been found with defects or signs of wear that may compromise safety."
        },
        "rigging_condition": {
            "Good": "Lifting operations were executed without incidents or deviations, following all safety protocols.",
            "Bad": "Irregularities were observed during the lifting operation, including potential risks or procedural deviations."
        },
        "lashing_condition": {
            "Good": "All lashing materials have been checked and found in proper condition, suitable for safe securing of the cargo.",
            "Bad": "Lashing materials were found damaged, worn, or not properly installed, requiring correction or replacement."
        }
    }

    # Mapeamento de variáveis para nomes
    conditions_map = {
        "cargo_condition": cargo_condition,
        "lifting_condition": lifting_condition,
        "rigging_condition": rigging_condition,
        "lashing_condition": lashing_condition
    }

    # Itera e desenha
    for key, result in conditions_map.items():
        if not result or key not in condition_texts:
            continue

        cond_value = result.get(key, "Bad")  # Default para Bad se não encontrado
        text = condition_texts[key].get(cond_value, "")

        # Desenha o texto
        c.setFont("Helvetica", font_size)
        current_y = draw_paragraph(text, current_y, "Helvetica")
        current_y -= leading * 2  # Espaço entre seções

    # Desenha o separador no final
    separator_y = current_y + 30
    draw_separator_image(c, width, separator_y)
