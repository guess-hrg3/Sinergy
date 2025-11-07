import io
from html import unescape
from datetime import datetime
from lxml import etree as ET

from ws_client import get_authenticated_client
from utils.logger import setup_logger
from parsers.ficha_financeira import parse_ficha_financeira_xml
from database.ficha_financeira import upsert_ficha_financeira, get_cpfs_funcionarios

logger = setup_logger(__name__)

def get_dados_ficha_financeira(referencia: str = "102025", cpf: str = None):
    client = get_authenticated_client()
    try:
        if cpf:
            logger.debug(f"Buscando ficha financeira para CPF {cpf} e referência {referencia}")
            response = client.service.GetDadosFuncionariosFichaFinanceira(referencia, cpf)
        else:
            logger.debug(f"Buscando ficha financeira geral para referência {referencia}")
            response = client.service.GetDadosFuncionariosFichaFinanceira(referencia)

        if not response:
            logger.warning(f"Resposta vazia do WebService para CPF={cpf or 'TODOS'}")
            return None

        xml_str = unescape(response)

        if xml_str.startswith('\ufeff'):
            xml_str = xml_str.encode('utf-8').decode('utf-8-sig')

        return xml_str

    except Exception as e:
        logger.error(f"Erro ao recuperar dados da ficha financeira (CPF={cpf or 'TODOS'}): {e}")
        return None


def gerar_referencias(inicio, fim):
    """Gera lista de referências no formato MMYYYY entre duas datas."""
    mes_inicio, ano_inicio = int(inicio[:2]), int(inicio[2:])
    mes_fim, ano_fim = int(fim[:2]), int(fim[2:])

    referencias = []
    data_atual = datetime(ano_inicio, mes_inicio, 1)

    while data_atual <= datetime(ano_fim, mes_fim, 1):
        referencias.append(data_atual.strftime("%m%Y"))
        if data_atual.month == 12:
            data_atual = datetime(data_atual.year + 1, 1, 1)
        else:
            data_atual = datetime(data_atual.year, data_atual.month + 1, 1)

    return referencias


def integrar_ficha_financeira():
    logger.info("Iniciando integração da ficha financeira por CPF e referência...")

    referencias = gerar_referencias("102025", "102025")
    cpfs = get_cpfs_funcionarios()

    for referencia in referencias:
        logger.info(f"Processando referência {referencia}...")
        for cpf in cpfs:
            logger.info(f" → Processando CPF {cpf} para referência {referencia}...")

            xml_str = get_dados_ficha_financeira(referencia=referencia, cpf=cpf)

            if not xml_str:
                logger.warning(f"Nenhuma ficha encontrada para CPF {cpf} na referência {referencia}")
                continue

            try:
                fichas_data = parse_ficha_financeira_xml(xml_str)

                for ficha_data in fichas_data:
                    upsert_ficha_financeira(ficha_data)

                logger.info(f"CPF {cpf} na referência {referencia} processado com sucesso.")

            except Exception as e:
                logger.error(f"Erro ao processar CPF {cpf} na referência {referencia}: {e}")

    logger.info("Integração finalizada para todas as referências e CPFs.")
