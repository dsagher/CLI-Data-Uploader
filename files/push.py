import psycopg2 as ps
from generate_ddl import dataset


def sql_push(column_lst):
    host = input('Host: ')
    dbname = input('DB name: ')
    user = input('User: ')
    password = input('Password: ')
    port = input('Port: ')
    table_name = input('Table Name: ')

    conn = ps.connect(host=host, dbname=dbname, user=user, 
                    password=password, port=port)
    
    column_definitions = ", ".join(column_lst)

    cur = conn.cursor()

    create_sql = f'''
                --sql
                CREATE TABLE IF NOT EXISTS {table_name} (
                {column_definitions}
                );   
        '''
    try:
        cur.execute(create_sql)

        for key, value in dataset.dicts.items():
        # Assuming 'key' is a column and 'value' is a list of tuples or lists of data to insert
            insert_values = ', '.join([str(v) for v in value])
            insert_statement = f'INSERT INTO {table_name} ({key}) VALUES ({insert_values})'

        cur.execute(insert_statement)
        conn.commit()


    except Exception as e:
        print(f'An error occured: {e}')
        conn.rollback()

    finally:
        cur.close()
        conn.close()
    


