from fastapi import FastAPI, Response
from febraceapi import athena
from febraceapi.query import make_query
import json

app = FastAPI()

LIMIT = 100  # default limit
queryResultLocation = 's3://mestrado-educacao/application-athena-query/'
awsProfile = 'febrace'
awsCatalog = 'AwsDataCatalog'


def parse_fields(fields: str) -> list:
    fields = fields.replace('"', '').replace("'", "")  # prevent sqlinjection
    return fields.replace(' ', '').split(',')


# gets Athena's right table's name
def get_table(name: str) -> str:
    with open('tables.json') as f:
        tables = json.load(f)
    if name not in tables:
        raise Exception("Table doesn't exists.")
    return tables[name]


@app.get('/{table}')
async def query_table(table: str, fields: str, response: Response,
                      filters: str = None, limit: int = LIMIT) -> dict:

    fields = parse_fields(fields)
    table = table.replace('"', '').replace("'", "")  # no sqlinjection :)
    a = athena.Athena(awsCatalog, 'education',
                      queryResultLocation, profile=awsProfile)
    if filters is not None:
        filters = json.loads(filters)
    print(filters)

    try:
        table = get_table(table)
        data = a.query(make_query(table, fields, filters, limit))
    except Exception as e:
        response.status_code = 400
        return {'error': str(e)}
    return data


@app.get('/{table}/cols')
async def columns(table: str, response: Response) -> dict:
    a = athena.Athena(awsCatalog, 'education',
                      queryResultLocation, profile=awsProfile)

    table = table.replace('"', '').replace("'", "")
    try:
        data = a.table_columns(get_table(table))
    except Exception as e:
        response.status_code = 404
        return {'error': str(e)}

    return data


@app.get('/')
async def root():
    return {'main': 'root'}
