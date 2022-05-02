__all__ = ["athena", "query"]

tables = {
    "docentes": "docentes_parquet",
    "escolas": "escolas_parquet",
    "matriculas": "matriculas-parquet",
    "turmas": "turmas_parquet",
}


def get_table(name: str) -> str:
    if name not in tables:
        raise Exception("Table doesn't exists")
    return tables[name]
