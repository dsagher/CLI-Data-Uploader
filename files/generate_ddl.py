from get_sub_type import (dataset, 
                          get_boolean, 
                          get_char, 
                          get_date, 
                          get_index, 
                          get_numeric)

def generate_ddl(response: list[dict], want_index: bool, precision_decision: list) -> list:

    '''
    This function takes in a list of dictionaries from get_type() in convert.py. The input is classifications of datatypes
    'Numeric', 'Boolean', 'Character', and 'Date. The classifications are then passed into their respective functions which 
    determine the correct datatype based on a series of conditionals.

    Input: ex. [{'column':'name', 'type': 'Character'}]
    
    Returns: A list of SQL DDL (Data Definition Language) with the appropriate datatypes per each column.
    
    '''

    # Final DDL statement list
    result = list()

    # Add index to list before iterating through fields
    result.append(get_index()) if want_index == True else None

    # Iterate through {'column': 'x', 'type': 'y'} response from get_type() and column in dataset.columns
    # pass values into respective functions based on classification to determine the each column's datatype
    for dct in response: 
        for field in dataset.columns:
            if dct['column'] == field and dct['type'] == 'Numeric':
                
                result.append(get_numeric(field, dataset.dicts[field], precision_decision))
                
            elif dct['column'] == field and dct['type'] == 'Character':
                
                result.append(get_char(field, dataset.dicts[field]))

            elif dct['column'] == field and dct['type'] == 'Boolean':
                
                result.append(get_boolean(field))

            elif dct['column'] == field and dct['type'] == 'Date':
                
                result.append(get_date(field, dataset.dicts[field]))

    return result
