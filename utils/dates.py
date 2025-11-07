from datetime import datetime

def parse_date(data_str):
    if not data_str:
        return None

    data_str = data_str.strip()
    formatos = [
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d",        # <-- novo formato
        "%Y-%m-%d %H:%M:%S", 
        "%Y-%m-%d %H:%M"
    ]

    for fmt in formatos:
        try:
            return datetime.strptime(data_str, fmt)
        except ValueError:
            continue

    return None
