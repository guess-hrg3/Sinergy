from database.connection import get_connection
from utils.logger import setup_logger

logger = setup_logger(__name__)

def upsert_beneficio(beneficio_data: dict):
    """
    Insere ou atualiza um benefício na tabela SINERGY_FUNCIONARIOS_BENEFICIOS.
    Usa como chave composta: matricula_funcionario + beneficio + data_inicio_beneficio.
    """
    columns = list(beneficio_data.keys())

    update_columns = [f"{col} = ?" for col in columns if col not in ("matricula_funcionario", "beneficio", "data_inicio_beneficio")]

    update_sql = f"""
        UPDATE SINERGY_FUNCIONARIOS_BENEFICIOS
        SET {', '.join(update_columns)}
        WHERE matricula_funcionario = ? AND beneficio = ? AND data_inicio_beneficio = ?
    """

    insert_sql = f"""
        INSERT INTO SINERGY_FUNCIONARIOS_BENEFICIOS ({', '.join(columns)})
        VALUES ({', '.join(['?' for _ in columns])})
    """

    values_update = [beneficio_data[col] for col in columns if col not in ("matricula_funcionario", "beneficio", "data_inicio_beneficio")]
    values_update.extend([
        beneficio_data["matricula_funcionario"],
        beneficio_data["beneficio"],
        beneficio_data["data_inicio_beneficio"]
    ])
    values_insert = [beneficio_data[col] for col in columns]

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(update_sql, values_update)

        if cursor.rowcount == 0:
            cursor.execute(insert_sql, values_insert)

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Erro ao inserir/atualizar benefício (matrícula {beneficio_data.get('matricula_funcionario')}): {e}")
