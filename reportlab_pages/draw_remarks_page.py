from .utils.draw_commons_images import draw_separator_image, draw_header, draw_footer
from .utils.draw_wrapped_text import draw_wrapped_text
from .utils.draw_page_number import draw_page_number
from querys.get_dados_comments import get_dados_comments

def draw_remarks_page(c, width, height, cod_atividade, demanda_id):
    draw_header(c, width, height)
    draw_footer(c, width)
    draw_page_number(c, width)
    print('draw_cargo')

    if cod_atividade == "2":
        title = "10. QHSE REMARKS / POINTS TO IMPROVE"
    else:
        title = "11. QHSE REMARKS / POINTS TO IMPROVE"

    title_font = "CooperBlack"
    title_size = 20
    title_y = height - 150
    c.setFont(title_font, title_size)
    c.drawString(30, title_y, title)

    margin_x = 30
    max_width = width - (margin_x * 2)
    font_size = 13
    leading = 14

    def draw_paragraph(text, y, font_name, x=30):
        lines = draw_wrapped_text(
            c, text, x, y,
            max_width - (x - 30), font_name, font_size, leading
        )
        return lines[-1][2] - leading if lines else y - leading

    subtitle = "Following points of improvement and/or deviations have been noticed during our attendance on board:"
    current_y = draw_paragraph(subtitle, title_y - 30, "Calibri") - 20

    bullet_indent = 50
    symbol_offset = 15
    symbol_char = '⮚'

    # Busca comentários
    comment_result = get_dados_comments(demanda_id, 3, 6)
    # Esperado: ([['Comment 1'], ['Comment 2']], None)
    comment_data, _ = comment_result
    comments = [row[0] for row in comment_data] if comment_data else []

    # Se não houver comentários, mostra "No further comments..."
    if not comments:
        current_y -= 10
        c.setFont("Symbola", font_size)
        c.drawString(bullet_indent, current_y, symbol_char)
        current_y = draw_paragraph(
            "No further comments to be made.",
            current_y, "Calibri", x=bullet_indent + symbol_offset
        )
        current_y -= 6
    else:
        for comment_text in comments:
            # quebra de página se faltar espaço
            if current_y < 180:
                c.showPage()
                draw_header(c, width, height)
                draw_footer(c, width)
                draw_page_number(c, width)
                current_y = height - 150

            current_y -= 10
            c.setFont("Symbola", font_size)
            c.drawString(bullet_indent, current_y, symbol_char)
            current_y = draw_paragraph(
                comment_text,
                current_y, "Calibri", x=bullet_indent + symbol_offset
            )
            current_y -= 6

    # Espaço extra e separador
    separator_y = current_y + 30
    draw_separator_image(c, width, separator_y)
