# services/data_loaders.py

from querys.get_dados_demanda import get_dados_demanda
from querys.get_dados_cargo_table import get_dados_cargo_table
from querys.get_dados_lifting_table import get_dados_lifting_table
from querys.get_dados_lashing_table import get_dados_lashing_table
from querys.get_demanda_id import get_demanda_ids

def load_demanda_data(demanda_id):
    dados, error = get_dados_demanda(demanda_id)
    if error:
        return {
            "cliente": "-",
            "subject": "-",
            "title": "-",
            "vessel": "-",
            "cargos": "-",
            "dt_abertura": "-",
            "nm_demanda": "-",
            "location": "-",
            "bollards_aft": "-",
            "bollards_fwd": "-",
            "vessel_type": "-",
            "dwt": "-",
            "vessel_length": "-",
            "vessel_breadth": "-",
            "vessel_id": "-",
            "country_flag": "-",
            "imo_number": "-",
            "year_of_built": "-",
            "cod_atividade": "-",
            "id_pasta_gd_demanda": "-",
            "nome_demanda": "-",
        }, error
    return {
        "cliente": dados.get("cliente", "-"),
        "subject": dados.get("subject", "-"),
        "title": dados.get("title", "-"),
        "vessel": dados.get("vessel_name", "-"),
        "cargos": dados.get("cargos", "-"),
        "dt_abertura": dados.get("dt_abertura", "-"),
        "nm_demanda": dados.get("nome_demanda", "-"),
        "location": dados.get("location", "-"),
        "bollards_aft": dados.get("num_bollards_aft", "-"),
        "bollards_fwd": dados.get("num_bollards_fwd", "-"),
        "vessel_type": dados.get("vessel_type", "-"),
        "dwt": dados.get("dwt", "-"),
        "vessel_length": dados.get("vessel_length", "-"),
        "vessel_breadth": dados.get("vessel_breadth", "-"),
        "vessel_id": dados.get("vessel_id", "-"),
        "country_flag": dados.get("country_flag", "-"),
        "imo_number": dados.get("imo_number", "-"),
        "year_of_built": dados.get("year_of_built", "-"),
        "cod_atividade": dados.get("cod_atividade", "-"),
        "id_pasta_gd_demanda": dados.get("id_pasta_gd_demanda", "-"),
        "nome_demanda": dados.get("nome_demanda", "-"),
    }, None

def load_cargo_table(demanda_id):
    table_data, error = get_dados_cargo_table(demanda_id)
    if error or not table_data:
        return [["-", "-", "-", "-", "-", "-", "-", "-"]], error
    return table_data, None

def load_lifting_table(demanda_id):
    table_data, error = get_dados_lifting_table(demanda_id)
    if error or not table_data:
        return [["-", "-", "-", "-", "-"]], error
    return table_data, None

def load_lashing_table(demanda_id):
    table_data, error = get_dados_lashing_table(demanda_id)
    if error or not table_data:
        return [["-", "-", "-", "-", "-"]], error
    return table_data, None

def load_demanda_ids():
    demanda_data, error = get_demanda_ids()
    if error or not demanda_data:
        return [["-"]], error
    return demanda_data, None
