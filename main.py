from services.funcionarios import integrar_funcionarios
from services.beneficios import integrar_beneficios
from services.ficha_financeira import integrar_ficha_financeira
from services.marcacoes_ponto import integrar_marcacoes_ponto
from utils.logger import setup_logger 

logger = setup_logger(__name__)  


def main():
    integrar_funcionarios()
    #integrar_beneficios()
    #integrar_ficha_financeira()
    #integrar_marcacoes_ponto("2025-01-01", "2025-08-25")
    
    logger.info("Integração completa com sucesso.")

if __name__ == "__main__":
    main()

