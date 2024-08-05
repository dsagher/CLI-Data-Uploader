from re import fullmatch, IGNORECASE
from DataSet import dataset

def extract_values(lst: list[dict]) -> set[str]: 

    '''
    This function determines if a column only contains boolean values and adds it to a set to be used in get_type().
    It also populates the DataSet class instance that is used elsewhere in the code. 

    params:
        lst - list of dictionaries of the original csv dataset

    output:
        boolean_columns - a set of column names whose values are exclusively boolean 
    '''

    collect = set()
    keys = set()
    
    # Collect unique key-value pairs and unique keys
    for d in lst:
        for k,v in d.items():   
            collect.add((k,v))
            keys.add(k)

    # Identify boolean columns
    boolean_columns = set()

    for k in keys:
        values = {v.lower() for key, v in collect if key == k}
        if values.issubset({'0', '1', 'true', 'false', 't', 'f'}):
            boolean_columns.add(k)
    
    unique_values: dict = {k: set() for k in keys}

    # Populate unique_values with unique key-value pairs
    for key, value in collect:
        unique_values[key].add(value)

    # Add keys and values to Class Instance
    for key, values in unique_values.items():
        dataset.add_columns(key)
        dataset.add_unique_values(values)

    dataset.dicts = unique_values
    dataset.length = len(lst)
    
    return boolean_columns

def get_type(lst: list[dict]) -> list[dict]:

    '''
    This function outputs a list of dictionaries of column names and a classification of their datatype. 
    
    params:
        lst - list of dictionaries of the original csv dataset

    output:
        result -  a list of dictionaries containing {'column: column_name, 'type': 'datatype'}
    '''
    
    result = list()
    boolean_columns = extract_values(lst)
    processed_dct = dict()

    for dct in lst:
        
        for key, value in dct.items():
            if value != '':
                processed_dct[key] = value

    for key in processed_dct:

        if fullmatch(r'-?\d+(\.\d+)?([eE][-+]?\d+)?', processed_dct[key]) and key not in boolean_columns:
            # print('numeric', key)
            result.append({'column': key, 'type': 'Numeric'})    

        elif fullmatch(r'(?:\d{2})?\d{1,2}[-/:]\d{1,2}[-/:]\d{2}(?:\d{2})?', processed_dct[key]):
            result.append({'column': key, 'type': 'Date'}) 
            
        elif key in boolean_columns:
            result.append({'column': key, 'type': 'Boolean'})

        elif fullmatch(r'^(?!-?\d+(\.\d+)?([eE][-+]?\d+)?$).+', processed_dct[key], flags=IGNORECASE) and key not in boolean_columns:
            result.append({'column': key, 'type': 'Character'})
            # print('character', key)
        else:
            result.append({'column': key, 'type': 'Unknown'})   
            # print('unknown', key)     
             
    return result

def detect_index(lst: list[dict]) -> bool:
    
    '''
    This function detects whether an index column is present. 
    
    params: 
        lst - list of dictionaries of the original CSV dataset. 

    output:
        True if dataset present, False if not
    '''

    is_first_key_empty = all(len(dct) > 0 and list(dct.keys())[0] == '' for dct in lst)

    if is_first_key_empty:

        values = [dct.get('') for dct in lst]
        numbers = [str(i) for i in range(15)]
        has_expected_values = values[:15] == numbers

        unique_values = set(values)
        is_unique = len(unique_values) == len(values)
        
        if has_expected_values and is_unique:

            return True

    elif '' not in dataset.columns and not is_first_key_empty:

        return False
        
def del_index(lst: list[dict]) -> None:

    '''
    This function deletes the dataset from both the Dataset class instance and the list of dictionaries 
    of the original csv dataset. 

    input:
        lst - list of dictionaries of the original dataset.
    
    output:
        None.
    '''

    index = dataset.columns.index('')
    dataset.columns.pop(index)
    dataset.dicts.pop('')
    # Remove the empty string column from each dictionary in the list
    for dct in lst:
        if '' in dct:
            del dct['']