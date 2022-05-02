import json

from fastapi.testclient import TestClient
from febracepi import app

client = TestClient(app)

matriculas_query_files = ("filter1.json", "filter2.json", "filter3.json")

matriculas_query_results = ()


def test_query_matriculas():
    for path in matriculas_query_files:
        with open(f"queries_examples/{path}") as f:
            query = json.load(f)

        response = client.get(
            f"/matriculas/fields=nu_ano&filters={query}&limit=20"
        )
        assert response.status_code == 200
        # assert response.json() == {"msg": "Hello World"}
