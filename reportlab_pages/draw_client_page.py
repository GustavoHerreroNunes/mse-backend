from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import logging

from .utils.draw_commons_images import draw_footer, draw_header
from .utils.draw_wrapped_text import draw_wrapped_text
from utils.baixar_imagens import baixar_imagens  # ajuste conforme necessário
from querys.get_dados_photos_logo import get_dados_photos_logo

def draw_client_page(c: canvas.Canvas, width, height, cliente, title, nm_demanda, demanda_id):

    try:
        draw_header(c, width, height)
        draw_footer(c, width)
        print('draw_client')
        
        # === Texto superior ===
        draw_wrapped_text(
            c,
            "Issued by: MSE – Naval Consultancy & Survey",
            x=50,
            y=height - 130,
            max_width=width - 100,
            font_name="CooperBlack",
            font_size=12,
            leading=16
        )
        # Caminho absoluto até a raiz do projeto (assume que este script está em: generate_pdf/reportlab_pages/utils)
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "."))

        # Caminho da pasta de imagens dentro da raiz do projeto
        IMAGE_FOLDER = os.path.join(BASE_DIR, "pdf_static_images")

        # === Inserir MSE Logo ===
        mse_logo_path = os.path.join(IMAGE_FOLDER, "mse_logo.png")
        print(mse_logo_path)
        if os.path.exists(mse_logo_path):
            mse_image = ImageReader(mse_logo_path)
            mse_img_width, mse_img_height = mse_image.getSize()

            mse_scale = 0.5
            mse_img_width_scaled = mse_img_width * mse_scale
            mse_img_height_scaled = mse_img_height * mse_scale

            mse_x = (width - mse_img_width_scaled) / 2
            mse_y = height - 150 - mse_img_height_scaled - 10

            c.drawImage(
                mse_logo_path,
                mse_x,
                mse_y,
                width=mse_img_width_scaled,
                height=mse_img_height_scaled,
                preserveAspectRatio=True,
                mask='auto'
            )

        # === Texto abaixo do primeiro logo ===
        text_start_y = mse_y - 30
        draw_wrapped_text(
            c,
            f"Client: {cliente}",
            x=50,
            y=text_start_y,
            max_width=width - 100,
            font_name="CooperBlack",
            font_size=12,
            leading=18
        )

        # === Inserir Client Logo ===
        photo_url, error_packing = get_dados_photos_logo(demanda_id)
        if error_packing:
            photo_url = [["-"]]
            img_path = None
        else:
            imagens_salvas = baixar_imagens(photo_url, nome_pagina="cliente", demanda_id=demanda_id)
            img_path = imagens_salvas[0]

        if img_path:   
            if os.path.exists(img_path):
                client_image = ImageReader(img_path)
                client_img_width, client_img_height = client_image.getSize()

                client_scale = 0.5
                client_img_width_scaled = client_img_width * client_scale
                client_img_height_scaled = client_img_height * client_scale

                client_x = (width - client_img_width_scaled) / 2
                client_y = text_start_y - client_img_height_scaled - 20

                c.drawImage(
                    img_path,
                    client_x,
                    client_y,
                    width=client_img_width_scaled,
                    height=client_img_height_scaled,
                    preserveAspectRatio=True,
                    mask='auto'
                )

            # === Bloco final abaixo do segundo logo ===
            final_text_y = client_y - 50
        else:
            final_text_y = text_start_y - 20

        # Linha 1 - Our Reference
        draw_wrapped_text(
            c,
            "Our Reference:",
            x=50,
            y=final_text_y,
            max_width=width - 100,
            font_name="CooperBlack",
            font_size=14,
            leading=18
        )

        # Linha 2 - Número de referência
        draw_wrapped_text(
            c,
            nm_demanda,
            x=50,
            y=final_text_y - 24,
            max_width=width - 100,
            font_name="CooperBlack",
            font_size=20,
            leading=24
        )

        # Linha 3 - Title
        draw_wrapped_text(
            c,
            "Title:",
            x=50,
            y=final_text_y - 24 - 36,
            max_width=width - 100,
            font_name="CooperBlack",
            font_size=14,
            leading=18
        )

        # Linha 4 - Descrição
        draw_wrapped_text(
            c,
            title,
            x=50,
            y=final_text_y - 24 - 36 - 24,
            max_width=width - 100,
            font_name="CooperBlack",
            font_size=20,
            leading=24
        )

    finally:
        if img_path:
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