import logging
import sys
import os

def setup_logger(name=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Evita múltiplos handlers
    if logger.hasHandlers():
        return logger

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Diretório de logs
    os.makedirs("logs", exist_ok=True)

    # Log de sucesso/info/debug
    success_filter = lambda record: record.levelno <= logging.INFO
    fh_success = logging.FileHandler("logs/sinergy_success.log", encoding="utf-8")
    fh_success.setLevel(logging.DEBUG)
    fh_success.setFormatter(formatter)
    fh_success.addFilter(success_filter)
    logger.addHandler(fh_success)

    # Log de erros/warnings
    error_filter = lambda record: record.levelno >= logging.WARNING
    fh_error = logging.FileHandler("logs/sinergy_error.log", encoding="utf-8")
    fh_error.setLevel(logging.WARNING)
    fh_error.setFormatter(formatter)
    fh_error.addFilter(error_filter)
    logger.addHandler(fh_error)

    return logger
