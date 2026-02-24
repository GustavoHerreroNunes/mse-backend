from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def register_fonts():
    font_folder = os.path.join(os.path.dirname(__file__), "font")

    fonts = {
        "Montserrat": "Montserrat-Regular.ttf",
        "Montserrat-Bold": "Montserrat-Bold.ttf",
        "CooperBlack": "CooperBlack.ttf",
        "Calibri": "calibri.ttf",
        "Calibri-Bold": "calibri-bold.ttf",
        "Tahoma-Bold": "tahoma-bold.ttf",
        "Tahoma": "tahoma.ttf",
        "Symbola": "Symbola.ttf"
    }

    for name, file in fonts.items():
        path = os.path.join(font_folder, file)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fonte não encontrada: {path}")
        pdfmetrics.registerFont(TTFont(name, path))