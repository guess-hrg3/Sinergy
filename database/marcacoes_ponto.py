from database.connection import get_connection
from datetime import datetime

def upsert_marcacao_ponto(ponto_data: dict):
    """
    Insere ou atualiza uma marcação de ponto na tabela SINERGY_MARCACAO_PONTO.
    Atualiza também a coluna DATA_PARA_TRANSFERENCIA com a data/hora da operação.
    """
    columns = list(ponto_data.keys())

    # Adiciona a coluna DATA_PARA_TRANSFERENCIA
    insert_columns = columns + ["DATA_PARA_TRANSFERENCIA"]
    insert_placeholders = ['?' for _ in insert_columns]

    values_insert = [ponto_data[col] for col in columns]
    values_insert.append(datetime.now())

    insert_sql = f"""
        INSERT INTO SINERGY_MARCACAO_PONTO ({', '.join(insert_columns)})
        VALUES ({', '.join(insert_placeholders)})
    """

    # Update baseado em filial + matrícula + data + hora (chave composta)
    update_columns = [f"{col} = ?" for col in columns]
    update_columns.append("DATA_PARA_TRANSFERENCIA = ?")
    values_update = [ponto_data[col] for col in columns]
    values_update.append(datetime.now())

    update_sql = f"""
        UPDATE SINERGY_MARCACAO_PONTO
        SET {', '.join(update_columns)}
        WHERE filial_cnpj = ? AND matricula = ? AND data_batida = ? AND hora_batida = ?
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(update_sql, values_update + [
        ponto_data["filial_cnpj"],
        ponto_data["matricula"],
        ponto_data["data_batida"],
        ponto_data["hora_batida"]
    ])

    if cursor.rowcount == 0:
        cursor.execute(insert_sql, values_insert)

    conn.commit()
    cursor.close()
    conn.close()
