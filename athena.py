import boto3

'''
You mmust configure your aws credentials with aws cli.
(you may use a profile)

'''


class Athena:

    client = boto3.client('athena')

    def __init__(self, catalog: str, database: str, result_loc: str, profile: str=None):
        
        self.__catalog = catalog
        self.__database = database
        self.__profile = profile
        self.__result_loc = result_loc


        if profile is None:
            self.__client = boto3.client('athena')
        else:
            session = boto3.session.Session(profile_name=profile)
            self.__client = session.client('athena')

    @property
    def client(self):
        return self.__client

    def __wait_until_query_complete(self, query_id: str) -> str:
        r = self.client.get_query_execution(
                    QueryExecutionId = query_id
                )

        # waits for query result 
        while r['QueryExecution']['Status']['State'] in ('QUEUED', 'RUNNING'):
            r = self.client.get_query_execution(QueryExecutionId=query_id)
        
        return r['QueryExecution']['Status']['State']

    def __parse_data(self, brute_data: dict) -> dict:
        columns = brute_data['ResultSet']['ResultSetMetadata']['ColumnInfo']
        data = []
        for row in brute_data['ResultSet']['Rows']:
            d = {}
            for i, column in enumerate(columns):
                d[column['Name']] = row['Data'][i]['VarCharValue']
            data.append(d)
        return d

    def query(self, query_str: str) -> dict:
        r = self.client.start_query_execution(
                QueryString = query_str,
                QueryExecutionContext = {
                    'Database':self.__database,
                    'Catalog':self.__catalog
                },
                ResultConfiguration={
                    'OutputLocation':self.__result_loc
                }
            )
        status_result = self.__wait_until_query_complete(r['QueryExecutionId'])
        if status_result != 'SUCCEEDED':
            raise Exception("Query Error!")
        
        r = self.client.get_query_results(QueryExecutionId=r['QueryExecutionId'])
        return self.__parse_data(r)


