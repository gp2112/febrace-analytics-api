#from pyathena import connect
from pprint import pprint
import boto3
import time

session = boto3.session.Session(profile_name='febrace')
client = session.client('athena')


def query_status(query_id):
    r = client.get_query_execution(
                QueryExecutionId=query_id
            )
    return r['QueryExecution']['Status']['State']

def query_results(query_id):
    r = client.get_query_results(
                QueryExecutionId=query_id
            )
    return r

def get_schools(fields: list, limit: int=100) -> list:
    r = client.start_query_execution(
                QueryString=f'SELECT {", ".join(fields)} FROM escolas LIMIT {limit}',
                ResultConfiguration={"OutputLocation":"s3://mestrado-educacao/application-athena-query/"},
                QueryExecutionContext={'Database':'education', 'Catalog':'AwsDataCatalog'}

            )
    token = r.get('QueryExecutionId')
    t0 = time.time()
    status = query_status(token)
    print('waiting...')
    while time.time()-t0<400 and status in ('QUEUED', 'RUNNING'):
        time.sleep(1)
        status = query_status(token)
    r = query_results(token)
    pprint(r)
    return r
