from .draw_commons_images import draw_header, draw_footer
from .draw_page_number import draw_page_number

def start_new_page(c, width, height):
    """Inicia uma nova página padronizada (header, footer, número)."""
    c.showPage()
    draw_header(c, width, height)
    draw_footer(c, width)
    draw_page_number(c, width)
    return height - 150  # posição inicial consistente


def ensure_space(c, width, height, needed_space, current_y):
    """Garante que haja espaço suficiente, senão cria nova página."""
    bottom_margin = 60
    if current_y - needed_space < bottom_margin:
        return start_new_page(c, width, height)
    return current_y

