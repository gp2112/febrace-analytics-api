import strawberry
import typing

from fastapi import FastAPI
from strawberry.types import Info
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class School:
    id: int
    nome: str
    cidade: str
    estado: str
    tipo: str

def getSchools(info: Info):
    print(info.selected_fields[0].selections)
    return [
            School(id=1,
                    nome='abel',
                    cidade='Niteroi',
                    estado='RJ',
                    tipo='privada'
            )
        ]

@strawberry.type
class Query:
    schools: typing.List[School] = strawberry.field(resolver=getSchools)

schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix='/graphql')

@app.get('/')
def home():
    return {'teste':'oi'}
