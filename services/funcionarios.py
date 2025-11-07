from ws_client import get_authenticated_client
from utils.xml_helpers import parse_xml_response
from parsers.funcionarios import parse_funcionario_xml
from database.funcionarios import upsert_funcionario
from utils.logger import setup_logger 

logger = setup_logger(__name__)  

def get_dados_funcionarios():
    logger.info("Criando client SOAP...")
    client = get_authenticated_client()
    logger.info("Client criado. Chamando GetDadosFuncionarios()...")
    response = client.service.GetDadosFuncionarios()
    logger.info("Resposta recebida. Parseando XML...")
    return parse_xml_response(response, "dadosFuncionario")


def integrar_funcionarios():
    logger.info("Iniciando integração de funcionários com SinergyRH...")
    funcionarios = get_dados_funcionarios()

    if not funcionarios:
        logger.warning("Nenhum funcionário encontrado.")
        return

    for func_xml in funcionarios:
        func_data = parse_funcionario_xml(func_xml)
        try:
            upsert_funcionario(func_data)
            logger.info(f"Funcionário {func_data.get('func_num')} salvo no banco.")
        except Exception as e:
            logger.error(f"Erro ao salvar funcionário {func_data.get('func_num')}: {e}")
