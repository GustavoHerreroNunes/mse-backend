def draw_wrapped_text(c, text, x, y, max_width, font_name="Helvetica", font_size=12, leading=16, test_only=False):
    """
    Se test_only=True, apenas calcula as quebras e posições sem desenhar.
    """
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if c.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    if test_only:
        # Só retorna as linhas estimadas, com coordenadas fictícias
        return [(line, x, y - i * leading) for i, line in enumerate(lines)]

    c.setFont(font_name, font_size)
    line_positions = []
    for i, line in enumerate(lines):
        line_y = y - i * leading
        c.drawString(x, line_y, line)
        line_positions.append((line, x, line_y))

    return line_positions  # retorna a lista [(linha, x, y), ...]
