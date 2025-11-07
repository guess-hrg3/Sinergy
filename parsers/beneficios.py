from utils.dates import parse_date

def parse_beneficio_xml(xml_benef):
    def get_text(tag):
        el = xml_benef.find(tag)
        return el.text.strip() if el is not None and el.text else None

    return {
        "matricula_funcionario": get_text("matricula_funcionario"),
        "nome_funcionario": get_text("nome_funcionario"),
        "cpf_funcionario": get_text("cpf_funcionario"),
        "beneficiario": get_text("beneficiario"),
        "beneficio": get_text("beneficio"),
        "data_inicio_beneficio": parse_date(get_text("data_inicio_beneficio")),
        "status_beneficio": get_text("status_beneficio"),
        "nome_beneficio": get_text("nome_beneficio"),
        "codigo_ans_fornecedor": get_text("codigo_ans_fornecedor"),
        "cnpj_fornecedor": get_text("cnpj_fornecedor"),
        "nome_fornecedor": get_text("nome_fornecedor"),
        "codigo_cartao_beneficio_funcionario": get_text("codigo_cartao_beneficio_funcionario"),
        "id_matricula_sequencial": get_text("id_matricula_sequencial"),
        "nm_meses_vigencia": int(get_text("nm_meses_vigencia")) if get_text("nm_meses_vigencia") else None,
        "cpf_titular": get_text("cpf_titular"),
        "cod_beneficio_fornecedor": get_text("cod_beneficio_fornecedor"),
    }
