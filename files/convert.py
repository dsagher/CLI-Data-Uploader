import re
from DataSet import dataset

def extract_values(lst: list[dict]) -> set[str]: 

    '''
    This function takes list of dictionaries. Each dictionary is unpacked to collect unique key-value pairs.
    It identifies boolean columns and stores unique values for each key.

    Args:
    lists of dictionaries.

    Returns:
    
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
    unique_values: dict = {k: set() for k in keys}

    # Step 4: Populate unique_values with unique key-value pairs
    for key, value in collect:
        unique_values[key].add(value)

    # Step 5. Add keys and Values to Class Instance, and return True + column names for boolean columns.
    for key, values in unique_values.items():
        dataset.add_columns(key)
        dataset.add_unique_values(values)

    dataset.dicts = unique_values
    dataset.length = len(lst)
    
    return boolean_columns

def get_type(lst: list[dict]) -> list[dict]:

    first = lst[0]
    result = list()

    boolean_columns = extract_values(lst)
    
    for i in first:   
        

        if re.fullmatch(r'-?\d+(\.\d+)?([eE][-+]?\d+)?',first[i]) and i not in boolean_columns:
            result.append({'column': i, 'type': 'Numeric'})    

        elif re.fullmatch(r'(?:\d{2})?\d{1,2}[-/]\d{1,2}[-/]\d{2}(?:\d{2})?', first[i]):
            result.append({'column': i, 'type': 'Date'}) 
            
        elif i in boolean_columns:
            result.append({'column': i, 'type': 'Boolean'})

        elif re.fullmatch(r'(?!(?:-?\d+)$)(?!(?:-?\d+\.\d+)$)(?!(?:(true|false|t|f)$)).+', first[i], flags=re.IGNORECASE):
            result.append({'column': i, 'type': 'Character'})

        else:
            result.append({'column': i, 'type': 'Unknown'})        
             
    return result

def detect_index(lst: list[dict]) -> bool:
    '''
    Remove input from this function and put it in main. 
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

    index = dataset.columns.index('')
    dataset.columns.pop(index)
    dataset.dicts.pop('')
    # Remove the empty string column from each dictionary in the list
    for dct in lst:
        if '' in dct:
            del dct['']