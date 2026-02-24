from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import logging
import os
from reportlab.lib.utils import ImageReader

from .utils.draw_commons_images import draw_separator_image, draw_header, draw_footer
from .utils.draw_wrapped_text import draw_wrapped_text
from .utils.ai_lashing_condition import ai_lashing_condition
from querys.get_dados_lashing_condition import get_dados_lashing_condition
from querys.get_dados_comments import get_dados_comments
from querys.get_dados_photos import get_dados_photos
from utils.baixar_imagens import baixar_imagens
from .utils.draw_page_number import draw_page_number
from .utils.commons import ensure_space

def draw_lashing_page(c, width, height, demanda_id, table_data, figure_number):

    draw_header(c, width, height)
    draw_footer(c, width)
    draw_page_number(c, width)

    print('draw_lashing')

    title = "8. LASHING APPLIANCES & EQUIPMENT"
    title_font = "CooperBlack"
    title_size = 20
    title_y = height - 150
    c.setFont(title_font, title_size)
    c.drawString(30, title_y, title)
    print("lashing items: ", table_data)
    margin_x = 30
    max_width = width - (margin_x * 2)
    font_size = 13
    leading = 14

    def draw_paragraph(text, y, font_name, x=30):
        lines = draw_wrapped_text(c, text, x, y, max_width - (x - 30), font_name, font_size, leading)
        return lines[-1][2] - leading if lines else y - leading

    subtitle = "The cargos were fitted with rigging elements, where terminal has provided the following materials:"
    current_y = draw_paragraph(subtitle, title_y - 30, "Calibri")

    # Cabeçalho
    table_headers = ["Quantity", "Description", "Capacity (WLL)", "Length (m)"]

    # Remove os campos desnecessários para a tabela (índice 4)
    table_data_4 = [row[:4] for row in table_data]

    # Ajustar os valores da tabela
    formatted_data = []
    for row in table_data_4:
        try:
            quantity = int(row[0])
            quantity_str = f"{quantity}X"
        except (ValueError, TypeError):
            quantity_str = f"{row[0]}X"

        description = row[1]

        capacity = row[2]
        try:
            float_capacity = float(capacity)
            capacity_str = f"{float_capacity} ton each" if quantity > 1 else f"{float_capacity} ton"
        except (ValueError, TypeError):
            capacity_str = f"{capacity}"

        length = row[3]

        formatted_data.append([quantity_str, description, capacity_str, length])

        data = [table_headers] + formatted_data

    # Criação da tabela
    col_widths = [2*cm, 3*cm, 3*cm, 2.5*cm]
    table = Table(data, colWidths=col_widths)

    style = TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Calibri'),
        ('FONT', (0, 1), (-1, -1), 'Calibri'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.8, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
    ])
    table.setStyle(style)

    # Centralizar horizontalmente
    table_width = sum(col_widths)
    table_x = (width - table_width) / 2

    # Mede altura real da tabela
    table_width, table_height = table.wrap(0, 0)
    table_x = (width - table_width) / 2
    table_y = current_y - table_height - 20

    # Desenha tabela
    table.drawOn(c, table_x, table_y)

    # Atualiza current_y para posição logo abaixo da tabela
    current_y = table_y - 40

    # Próximo título
    subtitle = "8.1 GENERAL CONDITION OF LASHING APPLIANCES"
    current_y = draw_paragraph(subtitle, current_y, "CooperBlack") - 20
    subtitle = "Following sections show the inspection finds/notes regarding overall observed condition of the lashing appliances."
    current_y = draw_paragraph(subtitle, current_y, "Calibri") - 20

    bullet_indent = 50
    symbol_offset = 15
    symbol_char = '⮚'
    index_figure = []

    for idx, row in enumerate(table_data, 1):
        quantity_items, description_items, capacity_items, _, id_items = row

        section_number = f"8.1.{idx}"
        header_line = f"{section_number} {quantity_items}X {description_items.upper()} ({capacity_items} TON)"

        data, erro = get_dados_lashing_condition(id_items, description_items)
        if erro:
            comments = [
                "Overall, the lashing material was determined to be in satisfactory operational condition.",
            ]
        else:
            comments = ai_lashing_condition(data, description_items)

        # Estima espaço
        estimated_comment_lines = len(comments) * (leading + 10)
        estimated_image_block = 200
        total_needed = 30 + estimated_comment_lines + estimated_image_block
        current_y = ensure_space(c, width, height, total_needed, current_y)

        current_y = draw_paragraph(header_line, current_y, "CooperBlack", x=30) - 10
        current_y = draw_paragraph("In this respect, as per visual inspection, the following was noted:", current_y, "Calibri") - 20

        for line in comments:
            c.setFont("Symbola", font_size)
            c.drawString(bullet_indent, current_y, symbol_char)
            current_y = draw_paragraph(line, current_y, "Calibri", x=bullet_indent + symbol_offset)
            current_y -= 10

        photo_url, error_packing = get_dados_photos(demanda_id, 3, 4, None, id_items)
        if error_packing:
            photo_url = [["-", "-", "-", "-", "-", "-"]]

        try:
            imagens_salvas = baixar_imagens(photo_url, nome_pagina="lashing", demanda_id=demanda_id)
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

            if total_images == 1:
                # Checa espaço antes
                current_y = ensure_space(c, width, height, image_height + 60, current_y)
                y = current_y - image_height - 20

                img_path = imagens_salvas[0]
                image = ImageReader(img_path)

                image_x = (width - image_width) / 2
                c.drawImage(image, image_x, y, width=image_width, height=image_height,
                            preserveAspectRatio=True, mask='auto')
                caption_text = f'Figure {figure_number} – Lashing materials #{idx}.'
                figure_number += 1

                index_figure.append({
                    "title": caption_text,
                    "page_num": c.getPageNumber(),  # corrigido, sem +2
                    "bookmark_key": "cargo"
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

                    # Garante espaço antes de cada linha de imagens
                    current_y = ensure_space(c, width, height, image_height + 60, current_y)
                    y = current_y - image_height - 20

                    if is_single_in_last_row:
                        x = (width - image_width) / 2

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
                            caption_text = f'Figure {figure_number} – Lashing materials #{idx}.'
                            figure_number += 1
                            index_figure.append({
                                "title": caption_text,
                                "page_num": c.getPageNumber(),
                                "bookmark_key": "cargo"
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

            comment_result = get_dados_comments(demanda_id, 3, 4, None, id_items)
            comment_data, _ = comment_result
            comment_text = comment_data[0][0] if comment_data else None
            if comment_text:
                current_y = ensure_space(c, width, height, 100, current_y)

                current_y -= 10
                c.setFont("Calibri-Bold", font_size)
                c.drawString(50, current_y, "Surveyor’s Note:")
                text_width = c.stringWidth("Surveyor’s Note:", "Calibri-Bold", 13)
                underline_y = current_y - 2
                c.setLineWidth(0.5)
                c.line(50, underline_y, 50 + text_width, underline_y)

                current_y -= 30
                wrapped = f"• {comment_text}"
                lines = draw_wrapped_text(c, wrapped, 70, current_y, width - 100,
                                          font_name="Calibri", font_size=13, leading=16)
                if lines:
                    current_y = lines[-1][2] - leading
                current_y -= 20

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
