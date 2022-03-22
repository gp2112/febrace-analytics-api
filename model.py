from pyathena import connect

def get_schools(fields: list, limit: int=0) -> list:
    cursor = connect(s3_staging_dir='s3://mestrado-educacao/application-athena-query/').cursor()
    if limit > 0:
        cursor.execute(f"SELECT {', '.join(fields)} FROM escolas_parquet LIMIT {limit}")
    else:
        cursor.execute("SELECT {', '.join(fields)} FROM escolas_parquet")
    return cursor.fetchall() 
