import csv
from convert import get_type, detect_index, del_index
from generate_ddl import generate_ddl
from get_sub_type import dataset
from re import fullmatch
from push import sql_push

'''

main() will call arg to ask user for file and arguments. 
file will then be passed into:

extract_unique_values() - adds column names and unique values to the DataSet class and returns a list of boolean columns
del_index() -

get_type()- get_type() will return statements of general data type classification to get_sub_type().

get_sub_type() - will determine which subtype to use, and/or ask the user what they want to use based off what options they have.
                results will be passed to generate_ddl()

generate_ddl() - will generate SQL data definition language and pass result to push()

push()- will use SQLalchemy to push to a Postgres server. 

'''


def main():

    # Open file and assign to lst as list[dicts]
    file = input('What is the file path? ')
    with open(file, 'r') as infile:
        reader = csv.DictReader(infile, lineterminator='')  
        lst = list(reader)

    
    # Get type classifications NUMERIC, CHARACTER, DATE, or BOOLEAN
    response: list[dict] = get_type(lst)
    
    # Get list of columns with decimal values that require exact precision 
    precision_lst = set()

    for k in dataset.dicts:
        for v in dataset.dicts[k]:
            if fullmatch(r'-?\d+\.\d+', v):
                precision_lst.add(f'{k}')

    if precision_lst:
        print(precision_lst)
        precision_decision: list = input(f'Which fields require precision? ').split(' ')
    else:
        precision_decision = None

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

    print(dataset.dicts)
    column_lst = generate_ddl(response, want_index, precision_decision)
    sql_push(column_lst)
    

if __name__ == '__main__':
    main()