import csv
import re
from pprint import pprint
from DataSet import DataSet


with open('input/taylor_swift_spotify.csv', 'r') as infile:
    reader = csv.DictReader(infile, lineterminator='')
    
    lst = list()
    for row in reader:
        lst.append(row)

dataset = DataSet()

def extract_unique_values(lst):

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
        values = {v for key, v in collect if key == k}
        if values.issubset({'0', '1'}):
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
        if key in boolean_columns:
            return True, boolean_columns
    

lst_of_dicts = [{'hello':'1'},{'hello':'0'},{'hey':'1'},{'hey':'1'}, {'who':'3'}]
print(extract_unique_values(lst_of_dicts))

def del_index():

    # Make Optional?
    if [''] in reader.fieldnames:
        del first[''] # Delete index if exists
    else:
        pass


def get_type(lst_of_dicts):

    first = lst_of_dicts[0]
    result = list()

    for i in first:   
        

        if re.fullmatch(r'-?[\d\.]+',first[i]) and extract_unique_values(first[i]) != True:
            result.append({'column': i, 'type': 'Numeric'})    

        # Get Date.
        elif re.fullmatch(r'(?:\d{2})?\d{1,2}-\d{1,2}-\d{2}(?:\d{2})?', first[i]):
            result.append({'column': i, 'type': 'Date'}) 
            
        elif re.fullmatch(r'(true|false|0|1)',first[i], flags=re.IGNORECASE) and extract_unique_values(first[i]) == True:
            result.append({'column': i, 'type': 'Boolean'})

        # Get Character. Add support to get rid of only ints and floats
        elif re.fullmatch(r'(?!(?:-?\d+)$)(?!(?:-?\d+\.\d+)$)(?!(?:(true|True|TRUE|false|False|FALSE)$)).+', first[i]):
            result.append({'column': i, 'type': 'Character'}) 
        
             
    return result

# get_type(lst)
# extract_unique_values(lst)
# print(type(lst))