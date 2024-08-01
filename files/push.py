import sqlalchemy as sa

def sql_push(column_lst, lst):
    host = input('Host: ')
    dbname = input('DB name: ')
    user = input('User: ')
    password = input('Password: ')
    port = input('Port: ')
    table_name = input('Table Name: ')

    db_url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

    engine = sa.create_engine(db_url)
    connection = engine.connect()

    metadata = sa.MetaData()

    columns = []
    for col in column_lst:
        col_name, col_type = col.split(' ', 1)
        
        if col_type.startswith('CHAR'):
            char_length = int(col_type.split('(')[1].strip(')'))
            col_type_obj = sa.CHAR(char_length)
        elif col_type.startswith('VARCHAR'):
            col_type_obj = sa.String
        elif col_type == 'TEXT':
            col_type_obj = sa.Text
        elif col_type == 'BOOLEAN':
            col_type_obj = sa.Boolean
        elif col_type == 'DATE':
            col_type_obj = sa.Date
        elif col_type == 'TIME':
            col_type_obj = sa.Time
        elif col_type == 'TIMESTAMP':
            col_type_obj = sa.TIMESTAMP
        elif col_type == 'SMALLINT':
            col_type_obj = sa.SmallInteger
        elif col_type == 'INT' or col_type == 'INTEGER':
            col_type_obj = sa.Integer
        elif col_type == 'BIGINT':
            col_type_obj = sa.BigInteger
        elif col_type == 'REAL':
            col_type_obj = sa.REAL
        elif col_type == 'DOUBLE PRECISION':
            col_type_obj = sa.Float  # SQLAlchemy uses Float for double precision
        elif col_type.startswith('NUMERIC'):
                col_type_obj = sa.Numeric
        else:
            col_type_obj = sa.String  # Default type if not recognized

        columns.append(sa.Column(col_name, col_type_obj))
          
    table = sa.Table(table_name,metadata,*columns)

    metadata.create_all(engine)

    try:
        with engine.begin() as conn:
            conn.execute(table.insert(), lst)
        print(f"Data inserted successfully into {table_name}.")
    except Exception as e:
        print(f'An error occurred: {e}')
        conn.rollback()

    finally:
        connection.close()