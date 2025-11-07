import xml.etree.ElementTree as ET
from decimal import Decimal
from utils.logger import setup_logger
from utils.dates import parse_date

logger = setup_logger(__name__)

def parse_ficha_financeira_xml(xml_string):
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        logger.error(f"Erro ao parsear XML: {e}")
        return []

    fichas = []

    for item in root.findall('dadosFichaFinanceira'):
        def text(tag):
            el = item.find(tag)
            return el.text.strip() if el is not None and el.text else None

        def to_int(val):
            try:
                return int(val)
            except (TypeError, ValueError):
                return None

        def to_decimal(val):
            if not val:
                return None
            try:
                return Decimal(val.replace(',', '.'))
            except Exception:
                return None

        ficha = {
            'numero_matricula': to_int(text('numero_matricula')),
            'nome': text('nome'),
            'numero_cpf': text('numero_cpf'),
            'codigo_verba': to_int(text('codigo_verba')),
            'verba': text('verba'),
            'natureza_verba': text('natureza_verba'),
            'processo': text('processo'),
            'quantidade': to_decimal(text('quantidade')),
            'valor': to_decimal(text('valor')),
            'referencia': text('referencia'),
            'dt_calculo': parse_date(text('dt_calculo')),
            'data_pagamento': parse_date(text('data_pagamento')),
        }
        fichas.append(ficha)

    return fichas
