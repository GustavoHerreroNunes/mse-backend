from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm

from .utils.draw_commons_images import draw_separator_image, draw_header, draw_footer
from .utils.draw_page_number import draw_page_number
from .utils.commons import start_new_page 


def draw_packing_list_page(c, width, height, table_data, cliente):

    # Cabeçalho/rodapé da primeira página
    draw_header(c, width, height)
    draw_footer(c, width)
    draw_page_number(c, width)  # garante número na primeira página
    print('draw_packing')

    # Título principal
    title = "1. PACKING LIST"
    title_font = "CooperBlack"
    title_size = 20
    top_title_y = height - 150

    c.setFont(title_font, title_size)
    c.drawString(30, top_title_y, title)

    # Subtítulo
    subtitle_lines = [
        "The following cargo characteristics are based on the packing list as received",
        f"from {cliente}:"
    ]
    c.setFont("CooperBlack", 12)
    for i, line in enumerate(subtitle_lines):
        c.drawString(30, top_title_y - 30 - (i * 14), line)

    # Área disponível inicial
    current_y = top_title_y - 50 - len(subtitle_lines) * 14

    # Tabela
    headers = ["Name", "Weight (KG)", "Length (m)", "Width (m)", "Height (m)", "Additional info"]
    # Remove o campo cargo_type (índice 6)
    table_rows = [row[:6] for row in table_data]

    data = [headers] + table_rows

    table = Table(
        data,
        colWidths=[3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 5*cm],
        repeatRows=1,  # repete cabeçalho em cada parte/página
    )

    style = TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Calibri'),   # header
        ('FONT', (0, 1), (-1, -1), 'Calibri'),  # body
        ('FONTSIZE', (0, 0), (-1, -1), 11),

        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),   # header centralizado
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # Name
        ('ALIGN', (1, 1), (4, -1), 'CENTER'),   # numéricas
        ('ALIGN', (5, 1), (5, -1), 'CENTER'),   # Additional info

        ('GRID', (0, 0), (-1, -1), 0.8, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
    ])
    table.setStyle(style)

    # Paginação manual usando split quantas vezes forem necessárias
    left_margin = 30
    right_margin = 30
    bottom_margin = 60
    safe_gap = 40  # pedido: subir limite para 40px

    available_width = width - (left_margin + right_margin)

    remaining = table
    first_loop = True

    while True:
        # calcula altura disponível nesta página
        available_height = max(0, current_y - (bottom_margin + safe_gap))

        # se não cabe nada aqui (ex.: começamos muito embaixo), abre nova página
        if available_height <= 0 and not first_loop:
            current_y = start_new_page(c, width, height)  # já desenha header, footer e número
            available_height = max(0, current_y - (bottom_margin + safe_gap))

        # quebra a tabela em (parte que cabe) + (restante)
        parts = remaining.split(available_width, available_height)

        # Caso extremo: uma única linha é mais alta que available_height.
        # Força nova página até caber (evita overflow).
        if not parts:
            current_y = start_new_page(c, width, height)
            first_loop = False
            continue

        head = parts[0]
        head.wrapOn(c, width, height)
        head.drawOn(c, left_margin, current_y - head._height)

        # Atualiza cursor após desenhar esta parte
        current_y = current_y - head._height - 20  # um pequeno espaçamento após a parte

        # Se ainda há restante, vamos para a próxima página e seguimos o loop
        if len(parts) > 1:
            remaining = parts[1]
            current_y = start_new_page(c, width, height)
            first_loop = False
            continue

        # Não há mais partes: encerramos a tabela
        break

    # Separator abaixo da última parte da tabela (abre nova página se faltar espaço)
    separator_needed = 30  # altura aproximada do separador
    if current_y - separator_needed < (bottom_margin + safe_gap):
        current_y = start_new_page(c, width, height)

    draw_separator_image(c, width, current_y - 10)
