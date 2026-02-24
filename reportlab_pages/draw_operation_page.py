import logging
from reportlab.lib.utils import ImageReader
import os

from .utils.draw_commons_images import draw_separator_image, draw_header, draw_footer
from .utils.draw_wrapped_text import draw_wrapped_text
from .utils.ai_rigging_condition import ai_rigging_condition
from querys.get_dados_comments import get_dados_comments
from querys.get_dados_photos import get_dados_photos
from querys.get_dados_ia_rigging import get_dados_ia_rigging
from utils.baixar_imagens import baixar_imagens
from .utils.draw_page_number import draw_page_number

def draw_operation_page(c, width, height, demanda_id, table_data, figure_number, cod_atividade):

    draw_header(c, width, height)
    draw_footer(c, width)
    draw_page_number(c, width)
    print('draw_operation')

    if cod_atividade == "2":
        title = "8. CARGOS OPERATION"
        title_number = 8
    else:
        title = "9. CARGOS OPERATION"
        title_number = 9
        
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
        lines = draw_wrapped_text(c, text, x, y, max_width - (x - 30), font_name, font_size, leading)
        return lines[-1][2] - leading if lines else y - leading
    
    def ensure_space(c, needed_space, current_y):
        bottom_margin = 60
        if current_y - needed_space < bottom_margin:
            c.showPage()
            draw_header(c, width, height)
            draw_footer(c, width)
            draw_page_number(c, width)
            return height - 140
        return current_y

    bullet_indent = 50
    symbol_offset = 15
    symbol_char = '⮚'
    index_figure = []

    subtitle = "The following pictures and comments are related to cargoes operation."
    current_y = draw_paragraph(subtitle, title_y - 30, "Calibri", 50) - 20

    for idx, row in enumerate(table_data, 1):
        _, weight, _, _, _, _, cargo_type, cargo_id = row

        
        section_number = f"{title_number}.1.{idx}"
        header_line = f"{section_number} {cargo_type.upper()} #{idx} ({weight} T)"

        data, erro = get_dados_ia_rigging(cargo_id)
        if erro:
            comments = [
                "No further comments to be made.",
            ]
        else:
            comments = ai_rigging_condition(data)

        # Estima espaço para: título + intro + comentários + imagens
        estimated_comment_lines = len(comments) * (leading + 10)
        estimated_image_block = 200
        total_needed = 30 + 20 + estimated_comment_lines + estimated_image_block
        current_y = ensure_space(c, total_needed, current_y)

        current_y = draw_paragraph(header_line, current_y, "CooperBlack", x=30) - 10
        current_y = draw_paragraph("In this respect, as per visual inspection, the following was noted:", current_y, "Calibri") - 20

        for line in comments:
            c.setFont("Symbola", font_size)
            c.drawString(bullet_indent, current_y, symbol_char)
            current_y = draw_paragraph(line, current_y, "Calibri", x=bullet_indent + symbol_offset)
            current_y -= 10

        photo_url, error_packing = get_dados_photos(demanda_id, 3, 2, cargo_id)
        if error_packing:
            photo_url = [["-", "-", "-", "-", "-", "-"]]

        try:
            imagens_salvas = baixar_imagens(photo_url, nome_pagina="narrative", demanda_id=demanda_id)
            image_width = 250
            image_height = 188
            image_spacing_x = 20
            image_spacing_y = 10

            x = margin_x
            y = current_y - 190
            images_in_row = 0
            first_image_x = None
            last_image_x = None
            total_images = len(imagens_salvas)

            if len(imagens_salvas) == 1:
                img_path = imagens_salvas[0]
                image = ImageReader(img_path)

                if y < 100:
                    c.showPage()
                    draw_header(c, width, height)
                    draw_footer(c, width)
                    draw_page_number(c, width)
                    x = margin_x
                    y = height - 120 - image_height - image_spacing_y

                image_x = (width - image_width) / 2
                c.drawImage(image, image_x, y, width=image_width, height=image_height,
                            preserveAspectRatio=True, mask='auto')
                caption_text = f'Figure {figure_number} – Lifting and discharge {cargo_type} #{idx}.'
                figure_number = figure_number + 1

                index_figure.append({
                    "title": caption_text,
                    "page_num": c.getPageNumber() + 2,
                    "bookmark_key": "operation"
                })
                c.setFont("Calibri-Bold", 11)
                c.setFillColorRGB(0, 0, 0.5)
                caption_y = y - 15
                c.drawCentredString(width / 2, caption_y, caption_text)

                c.setFillColorRGB(0, 0, 0)
                current_y = caption_y - 30

            else:
                for i, img_path in enumerate(imagens_salvas):
                    is_last_image = i == total_images - 1
                    remaining_images = total_images - i
                    is_single_in_last_row = remaining_images == 1 and images_in_row == 0

                    # Centraliza se for a última imagem sozinha
                    if is_single_in_last_row:
                        x = (width - image_width) / 2

                    if y < 100:
                        c.showPage()
                        draw_header(c, width, height)
                        draw_footer(c, width)
                        draw_page_number(c, width)
                        x = margin_x if not is_single_in_last_row else (width - image_width) / 2
                        y = height - 120 - image_height - image_spacing_y

                    image = ImageReader(img_path)
                    c.drawImage(image, x, y, width=image_width, height=image_height,
                                preserveAspectRatio=True, mask='auto')

                    if images_in_row == 0:
                        first_image_x = x
                    last_image_x = x
                    images_in_row += 1
                    x += image_width + image_spacing_x

                    next_image_overflows = x + image_width > width - margin_x

                    if next_image_overflows or is_last_image:
                        if is_last_image:
                            last_image_right = last_image_x + image_width
                            center_x = (first_image_x + last_image_right) / 2
                            caption_text = f'Figure {figure_number} – Cargo condition {cargo_type} #{idx}.'
                            figure_number += 1

                            index_figure.append({
                                "title": caption_text,
                                "page_num": c.getPageNumber() + 2,
                                "bookmark_key": "operation"
                            })
                            c.setFont("Calibri-Bold", 11)
                            c.setFillColorRGB(0, 0, 0.5)
                            caption_y = y - 15
                            c.drawCentredString(center_x, caption_y, caption_text)
                            c.setFillColorRGB(0, 0, 0)
                            current_y = caption_y - 30

                        images_in_row = 0
                        x = margin_x
                        y -= image_height + image_spacing_y
                        first_image_x = None
                        last_image_x = None
            
            comment_result = get_dados_comments(demanda_id, 3, 2, cargo_id)
            # Supondo que o retorno seja tipo: ([['Comment 2']], None)
            comment_data, _ = comment_result
            comment_text = comment_data[0][0] if comment_data else None
            if comment_text:
                if current_y < 180:
                    c.showPage()
                    draw_header(c, width, height)
                    draw_footer(c, width)
                    draw_page_number(c, width)
                    current_y = height - 150
                current_y = current_y - 10
                c.setFont("Calibri-Bold", font_size)
                c.drawString(50, current_y, "Surveyor’s Note:")
                # Mede a largura do texto para saber até onde sublinhar
                text_width = c.stringWidth("Surveyor’s Note:", "Calibri-Bold", 13)

                # Define a posição da linha (ligeiramente abaixo do texto)
                underline_y = current_y - 2  # 2 pts abaixo

                # Desenha a linha sublinhando o texto
                c.setLineWidth(0.5)
                c.line(50, underline_y, 50 + text_width, underline_y)

                current_y -= 30
                wrapped = f"• {comment_text}"
                lines = draw_wrapped_text(c, wrapped, 70, current_y, width - 100, font_name="Calibri", font_size=13, leading=16)
                if lines:
                    current_y = lines[-1][2] - leading
                current_y = current_y - 20

        finally:
            for img_path in imagens_salvas:
                try:
                    os.remove(img_path)
                except Exception:
                    logging.exception(f"Erro ao remover imagem: {img_path}")
            dir_path = os.path.dirname(imagens_salvas[0]) if imagens_salvas else None
            if dir_path and os.path.exists(dir_path):
                try:
                    os.rmdir(dir_path)
                except Exception:
                    logging.exception(f"Erro ao remover diretório: {dir_path}")
                    
    # Espaço extra entre o texto e o separador
    separator_y = current_y + 30
    draw_separator_image(c, width, separator_y)
    return index_figure, figure_number