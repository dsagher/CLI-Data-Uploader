import sqlalchemy as sa
from re import fullmatch, compile, search

def to_bool(key: str, lst: list[dict]) -> None:

    # Change bool strings into bool types
    for dct in lst:
        if dct[key] in ['True', 't', '1','true','TRUE']:
            dct[key] = True
        else:
            dct[key] = False
    
def to_null(lst: list[dict]) -> list[dict]:

    # Change null strings into null types
    processed_lst = []

    for dct in lst:

        processed_row = dict()
        for key, val in dct.items():
            if val.lower() in ['','na','null', '-']:
                processed_row[key] = None
            else:
                processed_row[key] = val

        processed_lst.append(processed_row)
    
    return processed_lst

def alchemy_type(ddl: list, lst: list[dict]) -> list:
    '''
    This function converts generated SQL DDL statements into SQLalchemy datatypes

    params:

    ddl - list of DDL statements
    lst - list of dictionaries of original data
    '''
    columns = list()

    type_pattern = (
        r'VARCHAR|CHAR\(\d+\)|TEXT|NUMERIC(?:\(\d+,\d+\))?'
        r'|INT|SMALLINT|BIGINT|REAL|DOUBLE PRECISION|SMALLSERIAL|'
        r'SERIAL|BIGSERIAL|DATE|TIMESTAMP|TIME|BOOLEAN'
    )
    match_pattern = rf'(.+?)\s+({type_pattern})'
    numeric_pattern = compile(r'NUMERIC(?:\((\d+),(\d+)\))?')
    
    for col in ddl:
        match = fullmatch(match_pattern, col)

        if match:
            col_name, col_type = match.groups()

            if col_type.startswith('CHAR'):
                char_length = int(search(r'\d+', col_type).group())
                col_type_obj = sa.CHAR(char_length)

            elif col_type == 'VARCHAR':
                col_type_obj = sa.String

            elif col_type == 'TEXT':
                col_type_obj = sa.Text

            elif col_type == 'BOOLEAN':
                to_bool(col_name, lst)
                col_type_obj = sa.Boolean

            elif col_type == 'DATE':
                col_type_obj = sa.Date

            elif col_type == 'TIME':
                col_type_obj = sa.Time
                
            elif col_type == 'TIMESTAMP':
                col_type_obj = sa.TIMESTAMP

            elif col_type == 'SMALLINT':
                col_type_obj = sa.SmallInteger

            elif col_type in ('INT', 'INTEGER'):
                col_type_obj = sa.Integer

            elif col_type == 'BIGINT':
                col_type_obj = sa.BigInteger

            elif col_type == 'REAL':
                col_type_obj = sa.REAL

            elif col_type == 'DOUBLE PRECISION':
                col_type_obj = sa.Float  

            elif numeric_pattern.match(col_type):

                match = numeric_pattern.match(col_type)

                if match.group(1) and match.group(2):
                    precision, scale = map(int, (match.group(1), match.group(2)))
                    col_type_obj = sa.Numeric(precision=precision, scale=scale)
                else:
                    col_type_obj = sa.Numeric  # Handle NUMERIC without precision/scale

            elif col_type == 'SMALLSERIAL':
                col_type_obj = sa.SmallInteger().with_variant(sa.Integer, 'postgresql')

            elif col_type == 'SERIAL':
                col_type_obj = sa.Integer().with_variant(sa.Integer, 'postgresql')

            elif col_type == 'BIGSERIAL':
                col_type_obj = sa.BigInteger().with_variant(sa.BigInteger, 'postgresql')

            else:
                col_type_obj = sa.String

            columns.append(sa.Column(col_name, col_type_obj))

    return columns

def sql_push(ddl: list, lst: list[dict]) -> None:

    '''
    This function gets user information on database, converts the types to SQLalchemy datatype objects,
    and pushes to database. 

    params:
        ddl - a list of ddl statements with column name and specified datatype
        lst - the original list of dictionaries of the csv dataset 
    '''
    # Get user database info
    host = input('Host: ')
    dbname = input('DB name: ')
    user = input('User: ')
    password = input('Password: ')
    port = input('Port: ')
    table_name = input('Table Name: ')

    db_url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

    # Create connection  
    engine = sa.create_engine(db_url)
    connection = engine.connect()
    metadata = sa.MetaData()

    # Convert to SQLalchemy datatypes
    columns = alchemy_type(ddl, lst)

    # Processes '' to None's
    processed_lst = to_null(lst)

    # Create table
    table = sa.Table(table_name,metadata,*columns)

    metadata.create_all(engine)

    try:
        with engine.begin() as conn:

            conn.execute(table.insert(), processed_lst)
        print(f"Data inserted successfully into {table_name}.")

    except Exception as e:
        print(f'An error occurred: {e}')
        conn.rollback()

    finally:
        connection.close()