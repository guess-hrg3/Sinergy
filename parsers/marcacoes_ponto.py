from utils.dates import parse_date
from utils.logger import setup_logger

logger = setup_logger(__name__)

def parse_marcacao_ponto_xml(xml_element):
    """
    Parser robusto para 'dadosMarcacaoPontoSinergy' ignorando namespaces.
    """
    def get_text(tag):
        el = xml_element.xpath(f".//*[local-name()='{tag}']")
        value = el[0].text if el else None
        logger.debug(f"Tag '{tag}': {value}")
        return value

    data = {
        "filial_cnpj": get_text("filial_cnpj"),
        "matricula": get_text("matricula"),
        "cpf": get_text("cpf"),
        "pis": get_text("pis"),
        "nome": get_text("nome"),
        "data_batida": parse_date(get_text("data_batida")),
        "hora_batida": get_text("hora_batida"),
        #"horas_trabalhadas": get_text("horas_trabalhadas"),
        "data_real_marcacao": parse_date(get_text("data_real_marcacao")),
    }

    #logger.debug(f"Dados parseados do ponto: {data}")
    return data
