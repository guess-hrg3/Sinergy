from database.connection import get_connection
from utils.logger import setup_logger
from datetime import datetime

logger = setup_logger(__name__)

def upsert_ficha_financeira(ficha_data: dict):
    from datetime import datetime

    columns = list(ficha_data.keys())
    key_columns = ("numero_matricula", "codigo_verba", "referencia", "dt_calculo")
    update_columns = [col for col in columns if col not in key_columns]

    try:
        conn = get_connection()
        cursor = conn.cursor()

       
        where_clause = " AND ".join([f"{col} = ?" for col in key_columns])
        select_sql = f"SELECT {', '.join(update_columns)} FROM SINERGY_FICHA_FINANCEIRA WHERE {where_clause}"
        key_values = [ficha_data[col] for col in key_columns]
        cursor.execute(select_sql, key_values)
        existing_row = cursor.fetchone()

        if existing_row:
           
            old_data = dict(zip(update_columns, existing_row))
            changes = {}
            for col in update_columns:
                if ficha_data.get(col) != old_data.get(col):
                    changes[col] = (old_data.get(col), ficha_data.get(col))

            if changes:
   
                update_sql = f"""
                    UPDATE SINERGY_FICHA_FINANCEIRA
                    SET {', '.join([f'{col} = ?' for col in changes.keys()])}, DATA_PARA_TRANSFERENCIA = ?
                    WHERE {where_clause}
                """
                values = list(ficha_data[col] for col in changes.keys())
                values.append(datetime.now())  
                values.extend(key_values)
                cursor.execute(update_sql, values)

                logger.info(f"Atualizado registro matrícula {ficha_data.get('numero_matricula')}. Mudanças: {changes}")
        else:
           
            ficha_data["DATA_PARA_TRANSFERENCIA"] = datetime.now()
            all_columns = list(ficha_data.keys())
            insert_sql = f"""
                INSERT INTO SINERGY_FICHA_FINANCEIRA ({', '.join(all_columns)})
                VALUES ({', '.join(['?' for _ in all_columns])})
            """
            insert_values = [ficha_data[col] for col in all_columns]
            cursor.execute(insert_sql, insert_values)

            logger.info(f"Inserido novo registro matrícula {ficha_data.get('numero_matricula')}")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Erro ao inserir/atualizar ficha financeira (matrícula {ficha_data.get('numero_matricula')}): {e}")



def get_cpfs_funcionarios():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT func_num_cpf FROM SINERGY_FUNCIONARIOS WHERE func_num_cpf IS NOT NULL")
        cpfs = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return cpfs
    except Exception as e:
        logger.error(f"Erro ao recuperar CPFs dos funcionários: {e}")
        return []
