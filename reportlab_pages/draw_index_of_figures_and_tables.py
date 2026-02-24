from reportlab.lib import colors

from .utils.draw_commons_images import draw_footer, draw_header, draw_separator_image
from .utils.draw_wrapped_text import draw_wrapped_text

def draw_index_of_figures_and_tables(c, width, height, figures_data, tables_data):

    draw_header(c, width, height)
    draw_footer(c, width)
    print('draw_index')

    margin_x = 30
    y = height - 120
    max_text_width = width - 2 * margin_x - 50

    def draw_section(title_text, index_data, y):
        title_font = "Calibri-Bold"
        title_size = 14
        index_font = "Tahoma"
        index_size = 11
        leading = 16

        c.setFont(title_font, title_size)
        c.setFillColor(colors.HexColor("#003399"))

        title_width = c.stringWidth(title_text, title_font, title_size)
        c.drawString((width - title_width) / 2, y, title_text)

        y -= 30
        c.setFont(index_font, index_size)

        for entry in index_data:
            title = entry["title"]
            page_num = entry["page_num"]
            key = entry["bookmark_key"]

            estimated_lines = 1 + title.count(" ") // 5
            if y - estimated_lines * leading < 50:
                c.showPage()
                draw_header(c, width, height)
                draw_footer(c, width)
                y = height - 80
                c.setFont(title_font, title_size)
                c.setFillColor(colors.HexColor("#003399"))
                title_width = c.stringWidth(title_text, title_font, title_size)
                c.drawString((width - title_width) / 2, y, title_text)
                y -= 30
                c.setFont(index_font, index_size)

            line_data = draw_wrapped_text(c, title, margin_x, y, max_text_width, index_font, index_size, leading)

            for i, (line, lx, ly) in enumerate(line_data):
                text_width = c.stringWidth(line, index_font, index_size)
                dots_width = c.stringWidth(".", index_font, index_size)
                available_space = width - margin_x * 2 - text_width - 30
                num_dots = int(available_space // dots_width)
                dots = "." * num_dots

                c.setFillColor(colors.HexColor("#003399"))
                c.setFont(index_font, index_size)
                c.setStrokeColor(colors.HexColor("#003399"))
                c.setLineWidth(0.5)

                if i == len(line_data) - 1:
                    c.drawString(lx, ly, line)
                    underline_y = ly - 2
                    c.line(lx, underline_y, lx + text_width, underline_y)

                    page_num_x = width - margin_x - c.stringWidth(str(page_num), index_font, index_size)
                    dots_start_x = lx + text_width + 5
                    dots_end_x = page_num_x - 5
                    dot_width = c.stringWidth(".", index_font, index_size)
                    num_dots = int((dots_end_x - dots_start_x) // dot_width)
                    dots = "." * num_dots

                    c.drawString(dots_start_x, ly, dots)
                    c.drawString(page_num_x, ly, str(page_num))
                    line_top = line_data[0][2]
                    line_bottom = line_data[-1][2] - leading
                    c.linkAbsolute("", key, Rect=(margin_x, line_bottom, width - margin_x, line_top + leading))
                else:
                    c.drawString(lx, ly, line)
                    underline_y = ly - 2
                    c.line(lx, underline_y, lx + text_width, underline_y)

            y -= len(line_data) * leading

        return y

    y = draw_section("INDEX OF FIGURES", figures_data, y)
    y -= 40
    y = draw_section("INDEX OF TABLES", tables_data, y)

    # Inserir separador no fim do índice
    draw_separator_image(c, width, y)