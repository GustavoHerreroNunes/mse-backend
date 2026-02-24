from itertools import groupby
import logging
import os

from reportlab.lib.utils import ImageReader

from .utils.draw_commons_images import draw_header, draw_footer, draw_separator_image
from .utils.draw_wrapped_text import draw_wrapped_text
from .utils.ai_crane_condition import ai_crane_condition
from querys.get_dados_vessel_crane import get_dados_vessel_crane
from querys.get_dados_photos import get_dados_photos
from querys.get_dados_ia_crane import get_dados_ia_crane
from querys.get_dados_comments import get_dados_comments
from utils.baixar_imagens import baixar_imagens  # ajuste conforme necessário
from .utils.draw_page_number import draw_page_number

def draw_crane_page(c, width, height, vessel_name: str, demanda_id: int, vessel_id: int):
    """Generate the "Vessel's Crane" page.

    Parameters
    ----------
    c : reportlab.pdfgen.canvas.Canvas
        Canvas on which we are drawing.
    width, height : float
        Page dimensions.
    vessel_id : int
        Primary‑key of the vessel (used to query Tbl_vessel_crane / Tbl_swl_capacities).
    vessel_name : str
        Friendly vessel name (used in captions).
    demanda_id : int
        Id used for photo lookup.
    """

    draw_header(c, width, height)
    draw_footer(c, width)
    draw_page_number(c, width)
    print('draw_crane')

    crane_rows, err = get_dados_vessel_crane(vessel_id)
    if err:
        logging.warning(err)
        crane_rows = []

    bullet_points = []
    if crane_rows:
        crane_rows.sort(key=lambda r: r[0])
        for idx, (crane_id, rows_iter) in enumerate(groupby(crane_rows, key=lambda r: r[0]), start=1):
            bullet_points.append({"title": f"Ship’s Crane N.{idx}.", "description_lines": []})
            for row in rows_iter:
                _, _, radius_end, weight = row
                if radius_end == "-" or radius_end is None:
                    bullet_points[-1]["description_lines"].append(f"SWL {weight}t")
                else:
                    bullet_points[-1]["description_lines"].append(f"SWL {weight}t x {radius_end}M")
    else:
        bullet_points.append({
            "title": "Ship's Crane data unavailable.",
            "description_lines": ["No SWL data found for this vessel."]
        })

    title = "5. VESSEL'S CRANE"
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
        lines = draw_wrapped_text(c, text, x, y, max_width - (x - margin_x), font_name, font_size, leading)
        return lines[-1][2] - leading if lines else y - leading

    intro = (
        f"The Vessel Crane {vessel_name} has been applied for overall discharge operation. "
        "Moreover, the following characteristics were noted:"
    )
    current_y = draw_paragraph(intro, title_y - 30, "Calibri")

    bullet_indent = 30
    symbol_offset = 15
    text_indent = bullet_indent + symbol_offset
    symbol_char = '❖'
    current_y -= 20

    for point in bullet_points:
        c.setFont("Symbola", 16)
        c.drawString(bullet_indent, current_y, symbol_char)

        c.setFont("Calibri", 16)
        c.drawString(text_indent, current_y, point["title"])

        current_y -= 20

        for desc in point["description_lines"]:
            current_y = draw_paragraph(f"• {desc}", current_y, "Calibri", x=text_indent)
            current_y -= 5

        current_y -= 15

    subtitle = (
        "Moreover, as per visual inspection from outside and as further as could be seen, "
        "the following comments apply:"
    )
    current_y = draw_paragraph(subtitle, current_y, "Calibri")

    data, error = get_dados_ia_crane(demanda_id)
    if error:

        obs_bullets = [
            "No further comments to be made."
        ]
    else:
        obs_bullets = ai_crane_condition(data)
        print(obs_bullets)
    
    bullet_indent = 50
    symbol_offset = 15
    symbol_char = '⮚'
    current_y -= 20

    for line in obs_bullets:
        c.setFont("Symbola", font_size)
        c.drawString(bullet_indent, current_y, symbol_char)
        current_y = draw_paragraph(line, current_y, "Calibri", x=bullet_indent + symbol_offset)
        current_y -= 10

    photo_url, error_packing = get_dados_photos(demanda_id, 0, 4)
    if error_packing:
        photo_url = [["-", "-", "-", "-", "-", "-"]]
    
    index_figure = []
    
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
            try:
                img_path = imagens_salvas[0]
                image = ImageReader(img_path)
                
                # Se não couber mais na página, cria nova página
                if y < 100:
                    c.showPage()
                    draw_header(c, width, height)
                    draw_footer(c, width)
                    draw_page_number(c, width)
                    x = margin_x
                    y = height - 120 - image_height - image_spacing_y
                
                # Posição centralizada na página
                image_x = (width - image_width) / 2
                
                c.drawImage(
                    image,
                    image_x,
                    y,
                    width=image_width,
                    height=image_height,
                    preserveAspectRatio=True,
                    mask='auto'
                )

                # Legenda abaixo da imagem
                caption_text = 'Figure 2 – Ship’s Crane.'
                index_figure.append({
                                "title": caption_text,
                                "page_num": c.getPageNumber() + 2,
                                "bookmark_key": "crane"
                })
                c.setFont("Calibri-Bold", 11)
                c.setFillColorRGB(0, 0, 0.5)
                caption_y = y - 15
                caption_x = width / 2
                current_y = caption_y - 10
                c.drawCentredString(caption_x, caption_y, caption_text)

            except Exception:
                logging.exception(f"Erro ao desenhar imagem única: {img_path}")

        else:
            for idx, img_path in enumerate(imagens_salvas):
                try:
                    is_last_image = idx == total_images - 1
                    remaining_images = total_images - idx
                    is_single_in_last_row = remaining_images == 1 and images_in_row == 0

                    # Se for a última imagem sozinha na linha, centraliza
                    if is_single_in_last_row:
                        x = (width - image_width) / 2

                    # Se não couber mais na página, cria nova página
                    if y < 100:
                        c.showPage()
                        draw_header(c, width, height)
                        draw_footer(c, width)
                        draw_page_number(c, width)
                        x = margin_x if not is_single_in_last_row else (width - image_width) / 2
                        y = height - 120 - image_height - image_spacing_y

                    image = ImageReader(img_path)
                    c.drawImage(
                        image, x, y,
                        width=image_width,
                        height=image_height,
                        preserveAspectRatio=True,
                        mask='auto'
                    )

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
                            caption_text = 'Figure 2 – Ship’s Crane.'  
                            index_figure.append({
                                "title": caption_text,
                                "page_num": c.getPageNumber() + 2,
                                "bookmark_key": "crane"
                            })
                            c.setFont("Calibri-Bold", 11)
                            c.setFillColorRGB(0, 0, 0.5)
                            caption_y = y - 15
                            current_y = caption_y - 10
                            c.drawCentredString(center_x, caption_y, caption_text)

                        images_in_row = 0
                        x = margin_x
                        y -= image_height + image_spacing_y
                        first_image_x = None
                        last_image_x = None

                except Exception:
                    logging.exception(f"Erro ao desenhar imagem: {img_path}")
    
        comment_result = get_dados_comments(demanda_id, 0, 3)
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

            c.setFillColorRGB(0, 0, 0)
            c.setFont("Calibri-Bold", 13)
            current_y -= 10
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
                
        # Espaço extra entre o texto e o separador
        separator_y = current_y
        draw_separator_image(c, width, separator_y)

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
    
        return index_figure