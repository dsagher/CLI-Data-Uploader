import csv
import re
from pprint import pprint

# I'm in arg!
with open('input/taylor_swift_spotify.csv', 'r') as infile:
    reader = csv.DictReader(infile, lineterminator='')
    
    lst = list()
    for row in reader:
        lst.append(row)

class DataSet:
    
    column_lst = list()
    unique_lst = list()

    def add_columns(self, columns):
        self.column_lst.append(columns)
        self._columns = self.column_lst
    
    def add_unique_values(self, unique_values):
        self.unique_lst.append(unique_values)
        self._values = self.unique_lst
        
    @property   
    def columns(self):
        return self._columns
    
    @property
    def values(self):
        return self._values

dataset = DataSet()
def extract_unique_values(lst):

    '''
    This function takes in multiple lists of dictionaries via *args. Each dictionary is unpacked to collect unique key-value pairs.
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
    boolean_columns = {k for k in keys if {(k, 0), (k, 1)}.issubset(collect)}

    # Step 3: Create a dictionary to store unique values for each key
    unique_values = {k: set() for k in keys}

    # Step 4: Populate unique_values with unique key-value pairs
    for key, value in collect:
        unique_values[key].add(value)


    for key, values in unique_values.items():
        dataset.add_columns(key)
        dataset.add_unique_values(values)
        if key in boolean_columns:
            return True
        

    pprint(dataset.columns)
    pprint(dataset.values)

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
        

        if re.fullmatch(r'-?[\d\.]+',first[i]) and extract_unique_values != True:
            result.append({'column': i, 'type': 'Numeric'})    

        # Get Date.
        elif re.fullmatch(r'(?:\d{2})?\d{1,2}-\d{1,2}-\d{2}(?:\d{2})?', first[i]):
            result.append({'column': i, 'type': 'Date'}) 
            
        elif re.fullmatch(r'(true|false|0|1)',first[i], flags=re.IGNORECASE) and extract_unique_values == True:
            result.append({'column': i, 'type': 'Boolean'})

        # Get Character. Add support to get rid of only ints and floats
        elif re.fullmatch(r'(?!(?:-?\d+)$)(?!(?:-?\d+\.\d+)$)(?!(?:(true|True|TRUE|false|False|FALSE)$)).+', first[i]):
            result.append({'column': i, 'type': 'Character'}) 
        
             
    return result

get_type(lst)

extract_unique_values(lst)