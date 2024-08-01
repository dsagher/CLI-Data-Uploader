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
    cur = conn.cursor()

    
    column_definitions = ", ".join(column_lst)

    create_sql = f'''
                --sql
                CREATE TABLE IF NOT EXISTS {table_name} (
                {column_definitions}
                );   
        '''
    try:
        cur.execute(create_sql)

        # Need to add placeholders
        for key in dataset.dicts:
            value_lst = [(v,) for v in dataset.dicts[key]]
            cur.executemany(f'INSERT INTO {table_name} ({key}) VALUES (%s)', value_lst)

        conn.commit()


    except Exception as e:
        print(f'An error occured: {e}')
        conn.rollback()

    finally:
        cur.close()
        conn.close()
    


