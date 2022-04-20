
ops = {
    'equals':'=',
    'bigger':'>',
    'lower':'<',
    'diff':'!='
}

LIMIT = 90

def make_query(table: str, fields: list='*', filters: list=None, 
                    limit: int=LIMIT, legacy: bool=False) -> str:
    
    if fields is not None: fields=", ".join(fields)
    if filters is None: filters=list() 
    query = f'SELECT {fields} FROM "{table}"'
    
    if not legacy:
        query += ' WHERE ' + parse_where(filters, is_root=True)
        query += f' LIMIT {limit}'
        return query

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

def make_query_sql(query: dict):
    if 'field' not in query:
        raise Exception('Query Dictionary without "fields" param.')

    blds = "'" if type(query.get('equals')) is str else ''  
    
    sql = query['field']
    if 'bigger' in query and 'lower' in query:
        sql += f" BETWEEN {query['bigger']} AND {query['lower']}"
    elif 'equals' in query:
        sql += f"={blds}{query['equals']}{blds}"
    elif 'bigger' in query:
        sql += f">{query['bigger']}"
    elif 'lower' in query:
        sql += f"<{query['lower']}"
    elif 'diff' in query:
        sql += f"!={query['diff']}" 
    else:
        raise Exception('No valid operation selected.')
    
    return sql

# {'or':[{'and':[{'field':'nu_ano', 'value':2001}, {'field':'nu_usp', 'value':992}]}, {'value'}]}

def parse_where(query: dict, is_root: bool=False):
    # if it has 'field' paramter, it's a leaf
    if 'field' in query:
        return make_query_sql(query)

    if 'or' not in query and 'and' not in query:
        raise Exception('Query Dictionary without operation ("or" or "and")')

    op = list(query.keys())[0].upper()

    subqueries = []
    for sub_query in list(query.values())[0]:
        subqueries.append(parse_where(sub_query))
    sql = f' {op} '.join(subqueries)
    if not is_root and op == 'OR':
        sql = f'({sql})' # if it's OR and not root, use brackets
    
    return sql
     
