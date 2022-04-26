# Febrace Analytics API

## Requirements

if you don't have venv installed:\
`pip install virtualenv`\
then:\
`python -m venv .env`\
`source .env/bin/activate`\
`pip install -r requirements`

## Running
`cd src && uvicorn app:app`

## Query Sintax

### Fields

The fields paramter receives a simple list with the fields required for your query, divided by comma.

For example: `fields=nu_ano,id_matricula`

### Filters

The filters parameter must receive a JSON like string, whitch contains your query.

Every query can have a single query (leaf) and/or Operation Queries.

- The single query sintax is: `{"field":{field_name}, "{compare_operator}":{value}}`

- The operation queries sintax is: `{"{and/or}":[subquery1, subquery2, subquery3, ...]}`


For example:

```json
{
    "and":[
            {"or":[
                    {"field":"nu_ano", "bigger":2010},
                    {"field":"in_surdez", "equals":1}
                ]
            },
            {"field":"nu_ano_censo", "equals":2020}
    ]
}
```
is equivalent to `"... WHERE (nu_ano=2010 OR in_surdez=1) AND nu_ano_censo=2020"` in SQL
