from datetime import datetime

def format_date_with_ordinal(date: datetime):
    day = date.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return date.strftime(f"%B {day}{suffix}, %Y")