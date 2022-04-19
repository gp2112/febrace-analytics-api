from fastapi import FastAPI, Response
import athena
import json

app = FastAPI()

LIMIT = 100 #default limit
queryResultLocation = 's3://mestrado-educacao/application-athena-query/'
awsProfile = 'febrace'
awsCatalog = 'AwsDataCatalog'


def parse_fields(fields: str) -> list:
    fields = fields.replace('"', '').replace("'", "") #prevent sqlinjection
    return fields.replace(' ', '').split(',')

def make_query(table: str, fields: list='*', filters: list=None, limit: int=LIMIT) -> str:
    if fields is not None: fields=", ".join(fields)
    if filters is None: filters=list() 
    query = f'SELECT {fields} FROM "{table}"'
    
    if len(filters) > 0:
        query += ' WHERE'
    
    i = False
    for fil in filters:
        if i: query += ' AND'
        i = True
        
        # if the field is string, use blades
        blds = "'" if type(fil.get('equals')) is str else ''

        query += f" {fil['field']}"
        if 'bigger' in fil and 'lower' in fil:
            query += f" BETWEEN {fil['bigger']} AND {fil['lower']}"
        elif 'equals' in fil:
            query += f"={blds}{fil['equals']}{blds}"
        elif 'bigger' in fil:
            query += f">{fil['bigger']}"
        elif 'lower' in fil:
            query += f"<{fil['lower']}"
        elif 'diff' in fil:
            query += f"!={fil['diff']}"
    query += f" LIMIT {limit}"
    print(query)
    return query
    

# gets Athena's right table's name
def get_table(name: str) -> str:
    with open('tables.json') as f:
        tables = json.load(f)
    if name not in tables:
        raise Exception("Table doesn't exists.")
    return tables[name]


@app.get('/{table}')
async def query_table(table: str, fields: str, response: Response, 
                        filters: str=None, limit: int=LIMIT) -> dict:
    fields = parse_fields(fields)
    table = table.replace('"', '').replace("'", "") # no sqlinjection :)
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    if filters is not None:
        filters = json.loads(filters)
    print(filters)
       
    try:
        table = get_table(table)
        data = a.query(make_query(table, fields, filters, limit))
    except Exception as e:
        response.status_code = 400
        return {'error':str(e)}
    return data 

@app.get('/{table}/cols')
async def columns(table: str, response: Response) -> dict:
    a = athena.Athena(awsCatalog, 'education', queryResultLocation, profile=awsProfile)
    table = table.replace('"', '').replace("'", "")
    try:
        data = a.table_columns(get_table(table))
    except Exception as e:
        response.status_code = 404
        return {'error':str(e)}
    
    return data

@app.get('/')
async def root():
    return {'main':'root'}
