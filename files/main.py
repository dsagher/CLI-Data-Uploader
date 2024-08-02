import csv
from convert import get_type, detect_index, del_index
from generate_ddl import generate_ddl
from get_sub_type import dataset
from re import fullmatch
from push import sql_push

def main() -> None:

    '''
    This application takes in a CSV dataset, determines which datatypes to use, generates a SQL DDL statement,
    and pushes to a user-specified database. 
    '''
    
    # Open file and assign to lst as list[dicts]
    file = input('What is the file path? ')
    with open(file, 'r') as infile:
        reader = csv.DictReader(infile, lineterminator='')  
        lst: list[dict] = list(reader)

    
    # Get type classifications NUMERIC, CHARACTER, DATE, or BOOLEAN
    response: list[dict] = get_type(lst)
    
    # Prompt user to input list of columns that require precision
    precision_lst = set()

    for k in dataset.dicts:
        for v in dataset.dicts[k]:
            if fullmatch(r'-?\d+\.\d+', v):
                precision_lst.add(f'{k}')

    if precision_lst:
        print(precision_lst)
        precision_decision: list = input(f'Which fields require precision? ').split(' ')

    # Detect index in dataset and prompt user to delete it if present, and add one if not
    index_status: bool = detect_index(lst)

    if index_status == True:
        answer = input('Index column detected. Would you like to delete? (yes/y to confirm) ')
        if answer.lower() in ['yes', 'y']:
            del_index(lst)
            want_index = False
        else:
            del_index(lst)
            want_index = True
    else:
        answer = input('No index detected. Would you like to add one? (yes/y to confirm) ')
        want_index = True if answer.lower() in ['yes', 'y'] else False

    # Generate DDL statements
    column_lst = generate_ddl(response, want_index, precision_decision)

    # Push to SQL database
    sql_push(column_lst, lst)
    
if __name__ == '__main__':
    main()