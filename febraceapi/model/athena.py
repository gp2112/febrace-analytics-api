import boto3

"""
You mmust configure your aws credentials with aws cli.
(you may use a profile)

"""


class Athena:
    def __init__(
        self, catalog: str, database: str, result_loc: str, profile: str = None
    ):

        self.__catalog = catalog
        self.__database = database
        self.__profile = profile
        self.__result_loc = result_loc

        if profile is None:
            self.__client = boto3.client("athena")
        else:
            session = boto3.session.Session(profile_name=profile)
            self.__client = session.client("athena")

    @property
    def client(self):
        return self.__client

    # Waits for query to be completed
    def __wait_until_query_complete(self, query_id: str) -> str:
        r = self.client.get_query_execution(QueryExecutionId=query_id)

        # waits for query result
        while r["QueryExecution"]["Status"]["State"] in ("QUEUED", "RUNNING"):
            r = self.client.get_query_execution(QueryExecutionId=query_id)

        return r

    # __parse_data:
    # parse the brute data received from Athena
    #  for a more convenient dictionary format
    # check https://boto3.amazonaws.com/v1/documentation/api/
    # latest/reference/services/athena.html#Athena.Client.get_query_results

    def __parse_data(self, brute_data: dict) -> dict:
        columns = brute_data["ResultSet"]["ResultSetMetadata"]["ColumnInfo"]
        data = []
        for row in brute_data["ResultSet"][
            "Rows"
        ]:  # ignore the first row (columns names)
            d = {}
            for i, column in enumerate(columns):
                d[column["Name"]] = None
                if "VarCharValue" in row["Data"][i]:
                    d[column["Name"]] = row["Data"][i]["VarCharValue"]
            data.append(d)
        return data

    def table_columns(self, table_name: str) -> dict:
        r = self.client.get_table_metadata(
            CatalogName=self.__catalog,
            DatabaseName=self.__database,
            TableName=table_name,
        )
        if "TableMetadata" not in r:
            return None
        return r["TableMetadata"].get("Columns")

    # receives SQL string for querying into athena
    # If wait is set False, returns queryId and completes request async
    def query(self, query_str: str, wait: bool = True) -> list:
        r = self.client.start_query_execution(
            QueryString=query_str,
            QueryExecutionContext={
                "Database": self.__database,
                "Catalog": self.__catalog,
            },
            ResultConfiguration={"OutputLocation": self.__result_loc},
        )
        queryExId = r["QueryExecutionId"]

        if not wait:
            return [queryExId]

        status_result = self.__wait_until_query_complete(queryExId)
        status = status_result["QueryExecution"]["Status"]["State"]

        if status != "SUCCEEDED":
            raise Exception(
                status_result["QueryExecution"]["Status"]["StateChangeReason"]
            )

        r = self.client.get_query_results(QueryExecutionId=queryExId)
        data = self.__parse_data(r)

        # paginate
        while "NextToken" in r:
            r = self.client.get_query_results(
                QueryExecutionId=queryExId, NextToken=r["NextToken"]
            )
            data += self.__parse_data(r)
        return data[1:]
