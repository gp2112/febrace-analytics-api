from fastapi import FastAPI
import athena

app = FastAPI()

LIMIT = 100 #default limit
queryResultLocation = 's3://mestrado-educacao/application-athena-query/'
awsProfile = 'febrace'
awsCatalog = 'AwsDataCatalog'

def parse_fields(fields: str) -> list:
    return fields.replace(' ', '').split(',')

@app.get('/escolas')
async def escolas(fields: str, limit: int=LIMIT) -> dict:
    fields = parse_fields(fields)
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    
    try:
        data = a.query(f'SELECT {",".join(fields)} FROM "escolas_parquet" LIMIT {limit}')
    except Exception as e:
        return {'error':str(e)}, 404

    return data

@app.get('/matriculas')
async def matriculas(fields: str, limit: int=LIMIT) -> dict:
    fields = parse_fields(fields)
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    data = a.query(f'SELECT {",".join(fields)} FROM "matriculas-parquet" LIMIT {limit}')

    return data

@app.get('/docentes')
async def docentes(fields: str, limit: int=LIMIT) -> dict:
    fields = parse_fields(fields)
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    data = a.query(f'SELECT {",".join(fields)} FROM "docentes_parquet" LIMIT {limit}')
    
    return data

@app.get('/turmas')
async def turmas(fields: str, limit: int=LIMIT) -> dict:
    fields = parse_fields(fields)
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    data = a.query(f'SELECT {",".join(fields)} FROM "turmas_parquet" LIMIT {limit}')
    
    return data

@app.get('/')
async def root():
    return {'main':'root'}
