from reportlab.lib import colors

def draw_page_number(c, width):
    # Numeração no canto inferior direito (branco)
    c.setFont("CooperBlack", 10)
    c.setFillColor(colors.white)
    page_number_text = f"Pg. {c.getPageNumber() + 1}"
    c.drawRightString(width - 50, 40, page_number_text)
    c.setFillColor(colors.black)  # volta pro padrão depois, se quiser