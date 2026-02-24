from reportlab.lib import colors
import os

from .utils.draw_label_value import draw_label_value
from .utils.format_date_with_ordinal import format_date_with_ordinal


def draw_cover_page(c, width, height, cliente, subject, vessel, cargos, dt_abertura):
    
    # Caminho absoluto até a raiz do projeto (assume que este script está em: generate_pdf/reportlab_pages/utils)
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "."))

    # Caminho da pasta de imagens dentro da raiz do projeto
    IMAGE_FOLDER = os.path.join(BASE_DIR, "pdf_static_images")

    # === Inserir MSE Logo ===
    cover_image_path = os.path.join(IMAGE_FOLDER, "cover.jpeg")
    print(cover_image_path)
    if os.path.exists(cover_image_path):
        c.drawImage(cover_image_path, 0, 0, width=width, height=height)
    print('draw_cover')

    c.setFillColor(colors.white)
    c.setFont("Montserrat-Bold", 18)
    c.drawString(50, height - 350, "SURVEY REPORT")
    c.setFont("Montserrat", 12)

    # 📝 Desenhar dados na capa
    print(cliente)
    draw_label_value(c, 50, height - 390, "CLIENT:", cliente)
    print(subject)
    draw_label_value(c, 50, height - 420, "SUBJECT:", subject)
    print(vessel)
    draw_label_value(c, 50, height - 450, "VESSEL:", vessel)

    def limitar_cargos(texto, limite=40):
        return texto if len(texto) <= limite else texto[:limite - 3] + "..."

    cargos_limitado = limitar_cargos(cargos)

    print(cargos_limitado)
    draw_label_value(c, 50, height - 480, "CARGOS:", cargos_limitado)

    print(dt_abertura)
    draw_label_value(
        c, 50, height - 520, "Date of Issurance:", format_date_with_ordinal(dt_abertura)
    )

    c.showPage()
