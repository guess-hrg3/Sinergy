from lxml import etree as ET

def parse_xml_response(xml_string: str, tag_principal: str):
    """
    Recebe uma string XML e extrai os elementos sob a tag principal (como 'dadosFuncionario', 'dadosBeneficios', etc.).
    Retorna uma lista de elementos XML.
    """
    root = ET.fromstring(xml_string)
    return root.findall(tag_principal)