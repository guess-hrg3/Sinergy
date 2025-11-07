from database.connection import get_connection
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)

def upsert_funcionario(func_data: dict):
    """
    Insere ou atualiza um registro na tabela SINERGY_FUNCIONARIOS baseado no func_num.
    Só atualiza se houver diferença nos valores.
    """

    columns = list(func_data.keys())

    insert_columns = columns + ["DATA_PARA_TRANSFERENCIA"]
    insert_placeholders = ["?" for _ in insert_columns]
    values_insert = [func_data[col] for col in columns] + [datetime.now()]

    insert_sql = f"""
        INSERT INTO SINERGY_FUNCIONARIOS ({', '.join(insert_columns)})
        VALUES ({', '.join(insert_placeholders)})
    """

    update_columns = [f"{col} = ?" for col in columns if col != "func_num"]
    update_columns.append("DATA_PARA_TRANSFERENCIA = ?")

    values_update = [func_data[col] for col in columns if col != "func_num"]
    values_update.append(datetime.now())
    values_update.append(func_data["func_num"])

    update_sql = f"""
        UPDATE SINERGY_FUNCIONARIOS
        SET {', '.join(update_columns)}
        WHERE func_num = ?
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Verifica se o funcionário já existe
        cursor.execute(
            "SELECT TOP 1 * FROM SINERGY_FUNCIONARIOS WHERE func_num = ?",
            (func_data["func_num"],),
        )
        existing = cursor.fetchone()

        if not existing:
            # 2️⃣ Se não existe → insere
            cursor.execute(insert_sql, values_insert)
            logger.info(f"Novo funcionário inserido: {func_data['func_num']}")
        else:
            # 3️⃣ Se existe → compara
            columns_db = [desc[0] for desc in cursor.description]
            existing_dict = dict(zip(columns_db, existing))

            changed = False
            for col in columns:
                if col in existing_dict and str(existing_dict[col]) != str(func_data[col]):
                    changed = True
                    break

            if changed:
                cursor.execute(update_sql, values_update)
                logger.info(f"Funcionário atualizado: {func_data['func_num']}")
            else:
                logger.debug(f"Nenhuma alteração detectada: {func_data['func_num']}")

        conn.commit()

    except Exception as e:
        logger.error(f"Erro ao salvar funcionário {func_data.get('func_num')}: {e}")
        logger.debug(f"Valores enviados: {func_data}")
        raise

    finally:
        cursor.close()
        conn.close()
