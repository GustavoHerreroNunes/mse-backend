def draw_label_value(c, x, y, label, value):
    """Função utilitária para desenhar uma label (bold) + valor (normal)"""
    c.setFont("Montserrat-Bold", 12)
    c.drawString(x, y, label + " ")
    text_width = c.stringWidth(label + " ", "Montserrat-Bold", 12)
    c.setFont("Montserrat", 12)
    c.drawString(x + text_width + 1, y, value)