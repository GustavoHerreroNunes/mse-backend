from reportlab.lib import colors

from .utils.draw_commons_images import draw_separator_image, draw_header, draw_footer
from .utils.draw_page_number import draw_page_number

def draw_vessel_page(c, width, height, vessel, vessel_type, country_flag, imo_number, year_of_built, dwt, vessel_breadth, vessel_length):

    draw_header(c, width, height)
    draw_footer(c, width)
    print('draw_vessel')

    # Título principal
    title = "4. VESSEL"
    title_font = "CooperBlack"
    title_size = 20
    title_y = height - 150
    c.setFont(title_font, title_size)
    c.drawString(30, title_y, title)
    
    margin_x = 30
    max_width = width - (margin_x * 2)
    font_size = 13
    leading = 14

    vessel_highlight = f"{vessel_type} Ship"
    full_text = f'The vessel “{vessel}” was found to be a {vessel_highlight}, delivered in {year_of_built}.'

    # Divide o texto antes, durante e depois do highlight
    before, after = full_text.split(vessel_highlight)
    
    # Posição inicial
    y = title_y - 30
    x = 30

    c.setFont("Calibri", font_size)
    c.setFillColor(colors.black)
    
    # Desenha a parte antes do highlight
    c.drawString(x, y, before)
    x += c.stringWidth(before, "Calibri", font_size)

    # Desenha o trecho em vermelho
    c.setFillColor(colors.red)
    c.drawString(x, y, vessel_highlight)
    x += c.stringWidth(vessel_highlight, "Calibri", font_size)

    # Volta para preto e desenha o resto
    c.setFillColor(colors.black)
    c.drawString(x, y, after)

    current_y = y - leading - 20

    c.drawString(30, current_y, "In all, the following main particulars were recorded:")

    c.setFont("Calibri-Bold", 13)
    current_y = current_y - leading - 30
    c.drawString(60, current_y, "Vessel’s name:")
    c.drawString(240, current_y, f"{vessel}")
    current_y = current_y - leading
    c.drawString(60, current_y, "Type of vessel::")
    c.drawString(240, current_y, f"{vessel_type}")
    current_y = current_y - leading 
    c.drawString(60, current_y, "Flag:")
    c.drawString(240, current_y, f"{country_flag}")
    current_y = current_y - leading
    c.drawString(60, current_y, "IMO number:")
    c.drawString(240, current_y, f"{imo_number}")
    current_y = current_y - leading
    c.drawString(60, current_y, "Year of built:")
    c.drawString(240, current_y, f"{year_of_built}")
    current_y = current_y - leading 
    c.drawString(60, current_y, "LOA/Breadth:")
    c.drawString(240, current_y, f"{vessel_length} m/ {vessel_breadth} m")
    current_y = current_y - leading 
    c.drawString(60, current_y, "DWT (summer):")
    c.drawString(240, current_y, f"{dwt} MT")
    current_y = current_y - leading
    
    # Espaço extra entre o texto e o separador
    separator_y = current_y - 20
    draw_separator_image(c, width, separator_y)
    draw_page_number(c, width)
