import re
from DataSet import dataset
import csv

with open('input/taylor_swift_spotify.csv', 'r') as infile:
    reader = csv.DictReader(infile, lineterminator='')  
    lst = list(reader)

def extract_unique_values(lst: list) -> set: 

    '''
    This function takes list of dictionaries. Each dictionary is unpacked to collect unique key-value pairs.
    It identifies boolean columns and stores unique values for each key.

    Args:
    *args: Multiple lists of dictionaries.

    Returns:
    A dictionary where keys are the column names and values are sets of unique values for each column.
    '''

    collect = set()
    keys = set()
    
    # Step 1: Collect unique key-value pairs and unique keys
    for d in lst:
        for k,v in d.items():   
            collect.add((k,v))
            keys.add(k)

    # Step 2: Identify boolean columns - Set comprehension
    boolean_columns = set()

    for k in keys:
        values = {v.lower() for key, v in collect if key == k}
        if values.issubset({'0', '1', 'true', 'false', 't', 'f'}):
            boolean_columns.add(k)

    # Step 3: Create a dictionary to store unique values for each key
    unique_values = {k: set() for k in keys}

    # Step 4: Populate unique_values with unique key-value pairs
    for key, value in collect:
        unique_values[key].add(value)

    # Step 5. Add keys and Values to Class Instance, and return True + column names for boolean columns.
    for key, values in unique_values.items():
        dataset.add_columns(key)
        dataset.add_unique_values(values)

    dataset.dicts = unique_values
    
    return boolean_columns

extract_unique_values(lst)

def get_type(lst_of_dicts: list) -> list:

    first = lst_of_dicts[0]
    result = list()

    boolean_columns = extract_unique_values(lst_of_dicts)
    
    for i in first:   
        

        if re.fullmatch(r'-?(?:\d+)?(?:\.\d+)?',first[i]) and i not in boolean_columns:
            result.append({'column': i, 'type': 'Numeric'})    

        elif re.fullmatch(r'(?:\d{2})?\d{1,2}-\d{1,2}-\d{2}(?:\d{2})?', first[i]):
            result.append({'column': i, 'type': 'Date'}) 
            
        elif i in boolean_columns:
            result.append({'column': i, 'type': 'Boolean'})

        elif re.fullmatch(r'(?!(?:-?\d+)$)(?!(?:-?\d+\.\d+)$)(?!(?:(true|false|t|f)$)).+', first[i], flags=re.IGNORECASE):
            result.append({'column': i, 'type': 'Character'})

        else:
            result.append({'column': i, 'type': 'Unknown'})        
             
    return result


def del_index(lst: list) -> None:

    # Add functionality to add index if not exists

    if dataset.columns and '' in dataset.columns:
        index = dataset.columns.index('')

        is_in_all_dcts = all('' in dct for dct in lst)
        
        if is_in_all_dcts:

            values = [dct.get('') for dct in lst]
            numbers = [str(i) for i in range(15)]
            has_expected_values = values[:15] == numbers

            unique_values = set(values)
            is_unique = len(unique_values) == len(values)
            
            if has_expected_values and is_unique:
                # Confirm with the user
                answer = input('Empty column detected. It appears to be an index column. Is this correct? (yes/y to confirm) ')
                if answer.lower() in ['yes', 'y']:
                    # Remove the empty string column from DataSet class
                    dataset.columns.pop(index)
                    # Remove the empty string column from each dictionary in the list
                    for dct in lst:
                        if '' in dct:
                            del dct['']