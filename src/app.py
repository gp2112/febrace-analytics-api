from fastapi import FastAPI, Response
import athena

app = FastAPI()

LIMIT = 100 #default limit
queryResultLocation = 's3://mestrado-educacao/application-athena-query/'
awsProfile = 'febrace'
awsCatalog = 'AwsDataCatalog'

def parse_fields(fields: str) -> list:
    fields = fields.replace('"', '').replace("'", "") #prevent sqlinjection
    return fields.replace(' ', '').split(',')

@app.get('/escolas')
async def escolas(fields: str, limit: int, response: Response) -> dict:
    fields = parse_fields(fields)
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    
    try:
        data = a.query(f'SELECT {",".join(fields)} FROM "escolas_parquet" LIMIT {limit}')
    except Exception as e:
        response.status_code = 400
        return {'error':str(e)}

    return data

@app.get('/matriculas')
async def matriculas(fields: str, limit: int, response: Response) -> dict:
    fields = parse_fields(fields)
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    try:
        data = a.query(f'SELECT {",".join(fields)} FROM "matriculas-parquet" LIMIT {limit}')
    except Exception as e:
        response.status_code = 400
        return {'error':str(e)}
    return data

@app.get('/docentes')
async def docentes(fields: str, limit: int, response: Response) -> dict:
    fields = parse_fields(fields)
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    try:
        data = a.query(f'SELECT {",".join(fields)} FROM "docentes_parquet" LIMIT {limit}')
    except Exception as e:
        response.status_code = 400
        return {'error':str(e)}

    return data

@app.get('/turmas')
async def turmas(fields: str, limit: int, response: Response) -> dict:
    fields = parse_fields(fields)
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    try:
        data = a.query(f'SELECT {",".join(fields)} FROM "turmas_parquet" LIMIT {limit}')
    except Exception as e:
        response.status_code = 400
        return {'error':str(e)}
    return data

@app.get('/{table}/cols')
async def columns(table: str, response: Response) -> dict:
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    try:
        data = a.table_columns(table)
    except Exception as e:
        response.status_code = 404
        return {'error':str(e)}
    
    return data

@app.get('/')
async def root():
    return {'main':'root'}
