from convert import get_type, dataset, detect_index
import csv
from pprint import pprint
from re import fullmatch


def get_boolean(key, values):
    pass

def get_numeric(key: str, value: set, precision_decision: list) -> str:


    # Initialize
    dct = dict()
    lst = list()
    
    # Change value from set to list to iterate
    dct[key] = list(value)
    
    # Generator expressions
    cnt = max(len(i) for i in dct[key])
    mx = max(i for i in dct[key])
    mn = min(i for i in dct[key])
    dec = any('.' in i for i in dct[key])
    
     
    if dec:
        result = f'{key} NUMERIC,' if key in precision_decision else \
                 f'{key} REAL,' if cnt <= 6 else \
                 f'{key} DOUBLE PRECISION,' if cnt <= 15 else \
                 f'{key} Unknown for: {key}'  # Default to DOUBLE PRECISION if conditions are met

    else:
        int_mn, int_mx = int(mn), int(mx)
        result = f'{key} SMALLINT,' if -32768 <= int_mn and int_mx <= 32767 else \
                 f'{key} INT,' if -2147483648 <= int_mn and int_mx <= 2147483647 else \
                 f'{key} BIGINT,' if -9223372036854775808 <= int_mn and int_mx <= 9223372036854775807 else \
                 f'Unknown for: {key}'
        
    return result

def get_index() -> str:

    result = f'index SMALLSERIAL,' if dataset.length <= 32767 else \
                f'index SERIAL' if dataset.length <= 2147483647 else \
                f'index BIGSERIAL' if dataset.length <= 9223372036854775807 else None
    
    return result
        
def get_char(key, values):


    mx = max(len(i) for i in values)

    lengths = list(map(lambda x: len(x), values))
    same = all(v == lengths[0] for v in lengths)

    if same:
        result = f'{key} CHAR{[lengths[0]]},'
    else:
        result = f'{key} VARCHAR{[mx]},' if mx < 65535 else \
                 f'{key} TEXT'

    return result

def get_date(key: str, values: set) -> str:
    
    try: 
        date_lst = list()
        time_lst = list()
        unformatted_lst = list()
        timestamp_lst = list()

        # YYYY-MM-DD or YY-M-D
        date_pattern_1 = r'\d{2,4}[-/\.]\d{1,2}[-/\.]\d{1,2}'

        # DD-MM-YYYY or D-M-YY
        date_pattern_2 = r'\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}'

        # HH:MM:SS
        time_pattern = r'\d{2}:\d{2}:\d{2}'

        # Iterate through values list and pass values into respective lists, including a bucket for formats that don't fit.
        for v in list(values):
            
            if fullmatch(date_pattern_1, v) or fullmatch(date_pattern_2, v):
                date_lst.append(v)

            elif fullmatch(date_pattern_1 + r'\s' + time_pattern, v):
                timestamp_lst.append(v)

            elif fullmatch(time_pattern, v):
                time_lst.append(v)

            else:
                unformatted_lst.append(v)

        # Set result to appropriate DDL statement
        if unformatted_lst: # Recognize incorrect formats
            if date_lst:
                raise ValueError(f'{key} DATE Incorrect format: {unformatted_lst}')
            elif timestamp_lst:
                raise ValueError(f'{key} TIMESTAMP Incorrect format: {unformatted_lst}')
            elif time_lst:
                raise ValueError(f'{key} TIME Incorrect format: {unformatted_lst}')
            else:
                raise ValueError(f'{key} Unknown Format {unformatted_lst}')
        
        elif (date_lst and (time_lst or timestamp_lst)) or (timestamp_lst and time_lst):
            # Recognize correct but inconsistent formats
            raise ValueError(f'{key} Inconsistent format: {date_lst[0] if date_lst else ""} \
                                                          {time_lst[0] if time_lst else ""} \
                                                          {timestamp_lst[0] if timestamp_lst else ""}')
        
        
        # If lsts exists and all the values made it through the conditional 
        elif date_lst and len(date_lst) == len(values): 
            result = f'{key} DATE,'
        elif timestamp_lst and len(timestamp_lst) == len(values):
            result = f'{key} TIMESTAMP,'
        elif time_lst and len(time_lst) == len(values):
            result = f'{key} TIME,'
        else:
            result = f'{key} Unknown Format'                   

    except ValueError as e:
        result = str(e)

    return result
   
def generate_ddl(response: list[dict]) -> list:

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

            # elif dct['column'] == field and dct['type'] == 'Boolean':

            #     result.append(get_boolean(field, dataset.dicts[field]))
            elif dct['column'] == field and dct['type'] == 'Date':
                
                result.append(get_date(field, dataset.dicts[field]))

    return result

with open('input/taylor_swift_spotify.csv', 'r') as infile:
    reader = csv.DictReader(infile, lineterminator='')  
    lst = list(reader)

response = get_type(lst)
print(generate_ddl(response))