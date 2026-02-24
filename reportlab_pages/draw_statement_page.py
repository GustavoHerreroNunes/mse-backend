from datetime import datetime

from .utils.draw_commons_images import draw_separator_image, draw_header, draw_footer
from .utils.draw_wrapped_text import draw_wrapped_text
from .utils.draw_page_number import draw_page_number
from querys.get_dados_statement import get_dados_statement
from querys.get_dados_statement_cargo import get_dados_statement_cargo
from .utils.commons import start_new_page, ensure_space


# Função para colocar sufixo do dia (st, nd, rd, th)
def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def draw_statement_page(c, width, height, demanda_id, table_data_cargo):

    draw_header(c, width, height)
    draw_footer(c, width)
    draw_page_number(c, width)
    print('draw_statement')

    # Título principal
    title = "3. STATEMENT OF FACTS"
    title_font = "CooperBlack"
    title_size = 20
    title_y = height - 150
    c.setFont(title_font, title_size)
    c.drawString(30, title_y, title)

    margin_x = 30
    max_width = width - (margin_x * 2)
    font_size = 13
    leading = 14
    bullet_indent = 50
    symbol_offset = 15
    symbol_char = '⮚'  # seta

    # helper para imprimir parágrafo com quebra automática
    def draw_paragraph(text, y, font_name, needed_space=30, x=30):
        nonlocal c, width, height
        y = ensure_space(c, width, height, needed_space, y)
        lines = draw_wrapped_text(c, text, x, y, max_width - (x - 30), font_name, font_size, leading)
        return lines[-1][2] - leading if lines else y - leading

    # Texto introdutório
    subtitle = "For the sake of easier reference to parties concerned, the main events may be summarized as follows:"
    current_y = draw_paragraph(subtitle, title_y - 30, "Calibri")

    # Dados principais
    data, _ = get_dados_statement(demanda_id)

    # Agrupa cargos
    cargos_grouped = {}
    for idx, row in enumerate(table_data_cargo, 1):
        _, _, _, _, _, _, _, cargo_id = row
        data_cargo, _ = get_dados_statement_cargo(cargo_id)
        if data_cargo:
            cargos_grouped[f"Cargo #{idx}"] = data_cargo
    data["cargos"] = cargos_grouped

    eventos = []

    # Eventos principais
    for key, value in data.items():
        if key.endswith("_status") and value not in (None, "-", ""):
            ts_start_key = key.replace("_status", "_timestamp_start")
            ts_end_key = key.replace("_status", "_timestamp_end")

            ts_start_value = data.get(ts_start_key)
            ts_end_value = data.get(ts_end_key)

            if ts_start_value and ts_start_value not in ("-", None):
                try:
                    ts_start_dt = datetime.fromisoformat(ts_start_value)
                    ts_end_dt = datetime.fromisoformat(ts_end_value) if ts_end_value and ts_end_value not in ("-", None) else None
                except ValueError:
                    continue
                eventos.append((ts_start_dt, ts_end_dt, value, None))

    # Eventos por cargo
    for cargo_label, cargo_data in cargos_grouped.items():
        cargo_num = cargo_label.split("#")[-1].strip()
        for key, value in cargo_data.items():
            if key.endswith("_status") and value not in (None, "-", ""):
                ts_start_key = key.replace("_status", "_timestamp_start")
                ts_end_key = key.replace("_status", "_timestamp_end")

                ts_start_value = cargo_data.get(ts_start_key)
                ts_end_value = cargo_data.get(ts_end_key)

                if ts_start_value and ts_start_value not in ("-", None):
                    try:
                        ts_start_dt = datetime.fromisoformat(ts_start_value)
                        ts_end_dt = datetime.fromisoformat(ts_end_value) if ts_end_value and ts_end_value not in ("-", None) else None
                    except ValueError:
                        continue
                    eventos.append((ts_start_dt, ts_end_dt, value, cargo_num))

    # Ordena cronologicamente
    eventos.sort(key=lambda x: x[0])

    # Agrupa por data e imprime
    current_date = None
    for ts_start, ts_end, nome_evento, cargo_num in eventos:
        date_str = ts_start.strftime("%B {S}, %Y").replace("{S}", str(ts_start.day) + suffix(ts_start.day))
        if date_str != current_date:
            current_y -= leading
            current_y = draw_paragraph(f"{date_str}:", current_y, "Calibri-Bold", needed_space=leading + 40)
            current_date = date_str

        # monta horário
        if ts_end:
            time_str = f"{ts_start.strftime('%H:%M LT')} to {ts_end.strftime('%H:%M LT')}"
        else:
            time_str = ts_start.strftime("%H:%M LT")

        evento_str = nome_evento
        if cargo_num:
            evento_str += f" of Cargo #{cargo_num}"

        # garante espaço antes do evento
        current_y = ensure_space(c, width, height, 40, current_y)

        # desenha bullet + texto
        current_y -= 20
        c.setFont("Symbola", font_size)
        c.drawString(bullet_indent, current_y, symbol_char)
        c.setFont("Calibri", font_size)
        c.drawString(bullet_indent + symbol_offset, current_y, f"{time_str} – {evento_str}")

    # Espaço extra + separador
    current_y = ensure_space(c, width, height, 40, current_y)
    separator_y = current_y - 20
    draw_separator_image(c, width, separator_y)
