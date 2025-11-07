from datetime import datetime, timedelta
from ws_client import get_authenticated_client
from utils.logger import setup_logger
from parsers.marcacoes_ponto import parse_marcacao_ponto_xml
from database.marcacoes_ponto import upsert_marcacao_ponto
from utils.xml_helpers import parse_xml_response

logger = setup_logger(__name__)

def get_dados_marcacao_ponto(psReferenciaInicio: str, psReferenciaFim: str):
    client = get_authenticated_client()
    response = client.service.GetDadosMarcacaoPontoSinergy(
        psReferenciaInicio=psReferenciaInicio,
        psReferenciaFim=psReferenciaFim
    )
    return parse_xml_response(response, "dadosMarcacaoPontoSinergy")

def gerar_intervalos_mes_a_mes(inicio: str, fim: str):
    """
    Recebe strings YYYY-MM-DD e retorna lista de tuplas (inicio_mes, fim_mes) mês a mês.
    """
    data_inicio = datetime.strptime(inicio, "%Y-%m-%d")
    data_fim = datetime.strptime(fim, "%Y-%m-%d")

    intervalos = []
    atual = data_inicio

    while atual <= data_fim:
        primeiro_dia = atual.replace(day=1)
        if atual.month == 12:
            ultimo_dia = atual.replace(day=31)
        else:
            proximo_mes = atual.replace(day=28) + timedelta(days=4)  # garante ir pro próximo mês
            ultimo_dia = (proximo_mes - timedelta(days=proximo_mes.day)).replace(hour=0, minute=0, second=0)

        if ultimo_dia > data_fim:
            ultimo_dia = data_fim

        intervalos.append((
            primeiro_dia.strftime("%Y-%m-%d"),
            ultimo_dia.strftime("%Y-%m-%d")
        ))

        # vai pro próximo mês
        atual = ultimo_dia + timedelta(days=1)

    return intervalos

def integrar_marcacoes_ponto(inicio: str, fim: str):
    logger.info(f"Iniciando integração de marcações de ponto: {inicio} -> {fim}")

    intervalos = gerar_intervalos_mes_a_mes(inicio, fim)

    for psInicio, psFim in intervalos:
        logger.info(f"Processando intervalo {psInicio} -> {psFim}")
        pontos = get_dados_marcacao_ponto(psInicio, psFim)

        if not pontos:
            logger.warning(f"Nenhuma marcação de ponto encontrada para {psInicio} -> {psFim}")
            continue

        for ponto_xml in pontos:
            ponto_data = parse_marcacao_ponto_xml(ponto_xml)
            try:
                upsert_marcacao_ponto(ponto_data)
                logger.info(f"Marcação de ponto {ponto_data.get('matricula')} {ponto_data.get('data_batida')} {ponto_data.get('hora_batida')} salva.")
            except Exception as e:
                logger.error(f"Erro ao salvar marcação de ponto {ponto_data.get('matricula')}: {e}")

    logger.info("Integração de marcações de ponto finalizada.")

