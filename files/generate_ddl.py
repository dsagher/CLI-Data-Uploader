from get_sub_type import (dataset, 
                          get_boolean, 
                          get_char, 
                          get_date, 
                          get_index, 
                          get_numeric)

from convert import detect_index
from re import fullmatch



def generate_ddl(response: list[dict], lst) -> list:

    '''
    This function takes in a list of dictionaries from get_type() in convert.py. The input is classifications of datatypes
    'Numeric', 'Boolean', 'Character', and 'Date. The classifications are then passed into their respective functions which 
    determine the correct datatype based on a series of conditionals.

    Input: ex. [{'column':'name', 'type': 'Character'}]
    
    Returns: A list of SQL DDL (Data Definition Language) with the appropriate datatypes per each column.
    
    '''

    # Final DDL statement list
    result = list()

    # Set of columns with decimals
    precision_lst = set()

    for i, k in enumerate(dataset.dicts):
        for v in dataset.dicts[k]:
            if fullmatch(r'-?\d+\.\d+', v):
                precision_lst.add(f'{k}')

    # Display list of columns with decimals and prompt user to choose which columns require precision
    print(precision_lst)
    precision_decision = input(f'Which fields require precision? ').split(' ')


    # Detect index in dataset and prompt user to add one. 
    index_status = detect_index(lst)

    if index_status == 'No Index':
        want_index = input('No index detected. Would you like to add one? (y/yes): ')
        result.append(get_index()) if want_index.lower() in ['y', 'yes'] else None

    
    # Iterate through {'column': 'x', 'type': 'y'} response from get_type() and column in dataset.columns
    # pass values into respective functions based on classification to determine the each column's datatype
    for dct in response: 
        for field in dataset.columns:
            if dct['column'] == field and dct['type'] == 'Numeric':
                
                result.append(get_numeric(field, dataset.dicts[field], precision_decision))
                # pass

            elif dct['column'] == field and dct['type'] == 'Character':
                # pass
                result.append(get_char(field, dataset.dicts[field]))

            elif dct['column'] == field and dct['type'] == 'Boolean':
                # pass
                result.append(get_boolean(field, dataset.dicts[field]))
            elif dct['column'] == field and dct['type'] == 'Date':
                # pass
                result.append(get_date(field, dataset.dicts[field]))

    return result

