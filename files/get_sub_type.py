from convert import get_type, dataset, detect_index
import csv
from pprint import pprint
from re import fullmatch


def get_boolean(key, values):
    pass

def get_numeric(key: str, value: set, precision_decision: list, index: bool) -> str:


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


def get_date(key, values):
    
    try: 
        date_lst = list()
        time_lst = list()
        unformatted_lst = list()
        timestamp_lst = list()

        date_pattern_1 = r'\d{2,4}[-/\.]\d{1,2}[-/\.]\d{1,2}'
        date_pattern_2 = r'\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}'
        time_pattern = r'\d{2}:\d{2}:\d{2}'

        for v in list(values):
            
            if fullmatch(date_pattern_1, v) or fullmatch(date_pattern_2, v):
                date_lst.append(v)

            elif fullmatch(date_pattern_1 + r'\s' + time_pattern, v):
                timestamp_lst.append(v)

            elif fullmatch(time_pattern, v):
                time_lst.append(v)

            else:
                unformatted_lst.append(v)


        if date_lst and unformatted_lst:
            raise ValueError(f'{key} DATE Inconsistent format: {unformatted_lst}')
        elif timestamp_lst and unformatted_lst:
            raise ValueError(f'{key} TIMESTAMP Inconsistent format: {unformatted_lst}')
        elif time_lst and unformatted_lst:
            raise ValueError(f'{key} TIME Inconsistent format: {unformatted_lst}')
        elif date_lst and len(date_lst) == len(values):
            result = f'{key} DATE,'
        elif timestamp_lst and len(timestamp_lst) == len(values):
            result = f'{key} TIMESTAMP,'
        elif time_lst and len(time_lst) == len(values):
            result = f'{key} TIME,'

    except ValueError as e:
        result = e

    return result
   
def get_sub_type(response: list[dict]) -> list:

    result = list()
    precision_lst = set()

    for i, k in enumerate(dataset.dicts):
        for v in dataset.dicts[k]:
            if fullmatch(r'-?\d+\.\d+', v):
                precision_lst.add(f'{k}')

    # print(precision_lst)
    # precision_decision = input(f'Which fields require precision? ').split(' ')


    # index_status = detect_index(lst)
    
    # if index_status == 'No Index':
    #     want_index = input('No index detected. Would you like to add one? (y/yes): ')
    #     index = result.append(get_index()) if want_index.lower() in ['y', 'yes'] else None

    

    for dct in response: 
        for field in dataset.columns:
            if dct['column'] == field and dct['type'] == 'Numeric':
                
                # result.append(get_numeric(field, dataset.dicts[field], precision_decision, index))
                pass

            elif dct['column'] == field and dct['type'] == 'Character':
                pass
                # result.append(get_char(field, dataset.dicts[field]))

            # elif dct['column'] == field and dct['type'] == 'Boolean':

            #     result.append(get_boolean(field, dataset.dicts[field]))
            elif dct['column'] == field and dct['type'] == 'Date':
                
                result.append(get_date(field, dataset.dicts[field]))

    return result

with open('input/ed_sheeran_spotify.csv', 'r') as infile:
    reader = csv.DictReader(infile, lineterminator='')  
    lst = list(reader)

response = get_type(lst)
print(get_sub_type(response))