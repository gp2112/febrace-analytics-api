import strawberry
import typing

from fastapi import FastAPI
from strawberry.types import Info
from strawberry.fastapi import GraphQLRouter
import model

@strawberry.type
class School:
    id: int
    escola: str
    telefone: str
    uf: str

def getSchools(info: Info):
    selections = tuple(info.selected_fields[0].selections)
    fields = [s.name for s in selections]
    print(fields)
    return model.get_schools(fields, limit=5)

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