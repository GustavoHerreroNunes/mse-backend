from reportlab.pdfgen import canvas
import os

# Caminho absoluto até a raiz do projeto (assume que este script está em: generate_pdf/reportlab_pages/utils)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Caminho da pasta de imagens dentro da raiz do projeto
IMAGE_FOLDER = os.path.join(BASE_DIR, "pdf_static_images")

def draw_header(c: canvas.Canvas, width, height):
    header_image_path = os.path.join(IMAGE_FOLDER, "header.png")
    print(header_image_path)
    if os.path.exists(header_image_path):
        c.drawImage(header_image_path, 0, height - 100, width=width, height=100)

def draw_footer(c: canvas.Canvas, width):
    footer_image_path = os.path.join(IMAGE_FOLDER, "footer.png")
    print(footer_image_path)
    if os.path.exists(footer_image_path):
        c.drawImage(footer_image_path, 0, 0, width=width, height=100)

def draw_separator_image(c, width, y):
    separator_image_path = os.path.join(IMAGE_FOLDER, "separator.png")
    print(separator_image_path)
    image_width = 400
    image_height = 40
    if os.path.exists(separator_image_path) and y - image_height > 40:
        x = (width - image_width) / 2
        c.drawImage(separator_image_path, x, y - image_height - 10, width=image_width, height=image_height, preserveAspectRatio=True)
