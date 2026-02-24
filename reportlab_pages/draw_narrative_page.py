import os
from num2words import num2words
from reportlab.lib.utils import ImageReader

from .utils.draw_commons_images import draw_separator_image, draw_header, draw_footer
from .utils.draw_wrapped_text import draw_wrapped_text
from .utils.format_date_with_ordinal import format_date_with_ordinal
from utils.baixar_imagens import baixar_imagens  # ajuste conforme necessário
from querys.get_dados_attending_parties import get_dados_attending_parties
from querys.get_dados_comments import get_dados_comments
from querys.get_dados_photos import get_dados_photos
from .utils.draw_page_number import draw_page_number

def draw_narrative_page(c, width, height, cliente, vessel, location, quantity, dt_abertura, bollards_aft, bollards_fwd, demanda_id):
    draw_header(c, width, height)
    draw_footer(c, width)
    print('draw_narrative')

    photo_url, error_packing = get_dados_photos(demanda_id, 0, 1)
    if error_packing:
        photo_url = [
            ["-", "-", "-", "-", "-", "-"]
        ]
    # Legenda centralizada abaixo da imagem
    index_figure = []

    margin_x = 30
    max_width = width - (margin_x * 2)
    font_name = "Calibri"
    font_size = 13
    leading = 14

    title = "2. NARRATIVE/SURVEY CIRCUMSTANCES"
    title_font = "CooperBlack"
    title_size = 20
    title_y = height - 150
    c.setFont(title_font, title_size)
    c.drawString(margin_x, title_y, title)

    current_y = title_y - 30

    def draw_paragraph(text, y):
        lines = draw_wrapped_text(c, text, margin_x, y, max_width, font_name, font_size, leading)
        return lines[-1][2] - leading if lines else y - leading

    # Texto
    subtitle = (
        f"Following receipt of instructions, we liaised with {cliente} operation department as well as "
        f"terminal for survey alignments. In this respect, we were informed that Vessel {vessel} "
        f"was scheduled to be berthed at Port of {location}."
    )
    current_y = draw_paragraph(subtitle, current_y)

    quantity_extenso = num2words(quantity).lower()
    quantity_text = (
        f"Vessel was planned to load in (discharge) {quantity}x ({quantity_extenso}) volumes as break bulk."
    )
    current_y -= leading
    current_y = draw_paragraph(quantity_text, current_y)

    final_paragraph = (
        f"Therefore, on the operations dates we arrived at Port of {location} to supervise & inspect "
        "Lifting, Stowage and Lashing operation steps of the captioned cargo."
    )
    current_y -= leading
    current_y = draw_paragraph(final_paragraph, current_y)

    operation_date_text = f"The operation took place on the date: {format_date_with_ordinal(dt_abertura)}."
    current_y -= leading
    current_y = draw_paragraph(operation_date_text, current_y)

    position_text = (
        f"At the time of our attendance, the vessel was lying afloat fastened alongside by her Portside side at "
        f"Port of {location}, between the bollards No. {bollards_fwd} (fwd) and {bollards_aft} (aft)."
    )
    current_y -= leading
    current_y = draw_paragraph(position_text, current_y)

    # Baixa e desenha as imagens lado a lado
    try:
        imagens_salvas = baixar_imagens(photo_url, nome_pagina="narrative", demanda_id=demanda_id)
        image_width = 250  # para caber duas imagens lado a lado com margens
        image_height = 188
        image_spacing_x = 20
        image_spacing_y = 10

        # Começa um pouco abaixo do texto
        current_y -= (image_height + image_spacing_y)
        x = margin_x
        y = current_y

        images_in_row = 0  # para contar quantas imagens foram desenhadas na linha corrente
        first_image_x = None
        last_image_x = None

        if len(imagens_salvas) == 1:
            try:
                img_path = imagens_salvas[0]
                image = ImageReader(img_path)

                # Calcula centralização
                image_x = (width - image_width) / 2
                image_y = y  # y inicial fornecido

                c.drawImage(
                    image,
                    image_x,
                    image_y,
                    width=image_width,
                    height=image_height,
                    preserveAspectRatio=True,
                    mask='auto'
                )

                caption_text = f'Figure 1 - View of vessel "{vessel}" alongside at Port of {location}.'

                index_figure.append({
                    "title": caption_text,
                    "page_num": c.getPageNumber() + 2,
                    "bookmark_key": "narrative"
                })

                c.setFont("Calibri-Bold", 11)
                c.setFillColorRGB(0, 0, 0.5)
                caption_y = image_y - 15
                caption_x = width / 2  # centro da página
                c.drawCentredString(caption_x, caption_y, caption_text)

            except Exception as e:
                print(f"Erro ao desenhar imagem única: {img_path}\n{e}")
        else:
            # Bloco existente para múltiplas imagens
            for idx, img_path in enumerate(imagens_salvas):
                try:
                    image = ImageReader(img_path)
                    c.drawImage(
                        image,
                        x,
                        y,
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

                    if x + image_width > width - margin_x:
                        if images_in_row == 2 and (first_image_x is not None):
                            last_image_right = last_image_x + image_width
                            center_x = (first_image_x + last_image_right) / 2
                            caption_text = f'Figure 1 - View of vessel "{vessel}" alongside at Port of {location}.'
                            index_figure.append({
                                "title": caption_text,
                                "page_num": c.getPageNumber() + 2,
                                "bookmark_key": "narrative"
                            })
                            c.setFont("Calibri-Bold", 11)
                            c.setFillColorRGB(0, 0, 0.5)
                            caption_y = y - 15
                            c.drawCentredString(center_x, caption_y, caption_text)

                        images_in_row = 0
                        x = margin_x
                        y -= (image_height + image_spacing_y)
                        first_image_x = None
                        last_image_x = None

                except Exception as e:
                    print(f"Erro ao desenhar imagem: {img_path}\n{e}")
                
        # Caso reste uma linha com 2 imagens (ou exatamente 2 imagens na última linha), desenha a legenda
        if images_in_row == 2 and (first_image_x is not None):
            last_image_right = last_image_x + image_width
            center_x = (first_image_x + last_image_right) / 2
            caption_text = f'Figure 1 - View of Multi-Purpose vessel "{vessel}" alongside at the Commercial Quay – Port of {location}.'
            c.setFont("Calibri", 11)
            c.setFillColorRGB(0, 0, 1)  # azul
            caption_y = y - 15
            c.drawCentredString(center_x, caption_y, caption_text)

        # --- NOVA PÁGINA: Attending parties ---
        draw_page_number(c, width)
        c.showPage()  # inicia nova página
        draw_header(c, width, height)
        draw_footer(c, width)

        # Título "Attending parties:"
        c.setFont("Calibri-Bold", 13)
        attending_title = "Attending parties:"
        # Define a fonte e escreve o texto
        c.drawString(50, height - 150, attending_title)

        # Mede a largura do texto para saber até onde sublinhar
        text_width = c.stringWidth(attending_title, "Calibri-Bold", 13)

        # Define a posição da linha (ligeiramente abaixo do texto)
        underline_y = height - 152  # 2 pts abaixo

        # Desenha a linha sublinhando o texto
        c.setLineWidth(0.5)
        c.line(50, underline_y, 50 + text_width, underline_y)

        dados, erro = get_dados_attending_parties(demanda_id)
        if erro:
            c.setFont("Calibri", 13)
            c.setFillColorRGB(1, 0, 0)  # vermelho
            c.drawString(50, height - 180, f"Erro ao buscar dados: {erro}")
        else:
            font_size = 13
            leading = 18
            margin_x = 70
            current_y = height - 180

            c.setFont("Calibri", font_size)
            c.setFillColorRGB(0, 0, 0)

            for idx, (name, function, behalf) in enumerate(dados, start=1):
                line = f"{idx}. {name}, {function} on behalf of {behalf}."
                c.drawString(margin_x, current_y, line)
                current_y -= leading

        c.setFont("Calibri-Bold", 13)
        
        comment_result = get_dados_comments(demanda_id, 0, 1)
        # Supondo que o retorno seja tipo: ([['Comment 2']], None)
        comment_data, _ = comment_result
        comment_text = comment_data[0][0] if comment_data else None
        if comment_text:
            current_y = current_y - 20
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
        separator_y = current_y + 20
        draw_separator_image(c, width, separator_y)
        draw_page_number(c, width)

    finally:
        # Remove os arquivos e diretório
        for img_path in imagens_salvas:
            try:
                os.remove(img_path)
            except Exception as e:
                print(f"Erro ao remover imagem: {img_path}\n{e}")
        
        dir_path = os.path.dirname(imagens_salvas[0]) if imagens_salvas else None
        if dir_path and os.path.exists(dir_path):
            try:
                os.rmdir(dir_path)
            except Exception as e:
                print(f"Erro ao remover diretório: {dir_path}\n{e}")
        return index_figure