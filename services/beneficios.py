from ws_client import get_authenticated_client
from utils.xml_helpers import parse_xml_response
from parsers.beneficios import parse_beneficio_xml
from database.beneficios import upsert_beneficio
from utils.logger import setup_logger 

logger = setup_logger(__name__)

def get_dados_beneficios():
    client = get_authenticated_client()
    response = client.service.GetDadosBeneficios(qCpf="")  
    return parse_xml_response(response, "dadosBeneficios")

def integrar_beneficios():
    logger.info("Iniciando integração de benefícios com SinergyRH...")
    beneficios = get_dados_beneficios()

    if not beneficios:
        logger.warning("Nenhum benefício encontrado.")
        return

    for ben_xml in beneficios:
        ben_data = parse_beneficio_xml(ben_xml)
        try:
            upsert_beneficio(ben_data)
            logger.info(f"Benefício '{ben_data.get('beneficio')}' da matrícula {ben_data.get('matricula_funcionario')} salvo.")
        except Exception as e:
            logger.error(f"Erro ao salvar benefício: {e}")
