from convert import get_type, dataset, del_index
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
                 f'{key} Unknown,'  # Default to DOUBLE PRECISION if conditions are met
        
    # Have to make room for this one. I don't actually want {key} in there unless its ''.
    elif index == True:
        result = f'{key} SMALLSERIAL,' if dataset.row_count <= 32767 else \
                 f'{key} SERIAL' if dataset.row_count <= 2147483647 else \
                 f'{key} BIGSERIAL' if dataset.row_count <= 9223372036854775807 else None

    else:
        int_mn, int_mx = int(mn), int(mx)
        result = f'{key} SMALLINT,' if -32768 <= int_mn and int_mx <= 32767 else \
                 f'{key} INT,' if -2147483648 <= int_mn and int_mx <= 2147483647 else \
                 f'{key} BIGINT,' if -9223372036854775808 <= int_mn and int_mx <= 9223372036854775807 else \
                 f'Unknown for: {key}'
    
    return result


def get_char(key, values):
    pass

def get_date(key, values):
    pass

def get_sub_type(response: list[dict]) -> list:

    result = list()
    precision_lst = set()

    for i, k in enumerate(dataset.dicts):
        for v in dataset.dicts[k]:
            if fullmatch(r'-?\d+\.\d+', v):
                precision_lst.add(f'{k}')

    print(precision_lst)
    precision_decision = input(f'Which fields require precision? ').split(' ')

    for dct in response: 
        for field in dataset.columns:
            if dct['column'] == field and dct['type'] == 'Numeric':

                index_status = del_index(lst)  # Use dataset_dicts instead of lst if appropriate
                
                if index_status == 'No Index':
                    want_index = input('No index detected. Would you like to add one? (y/yes): ')
                    index = want_index.lower() in ['y', 'yes']
                else:
                    index = False
                
                result.append(get_numeric(field, dataset.dicts[field], precision_decision, index))
                
            
            # elif dct['column'] == field and dct['type'] == 'Character':

            #     result.append(get_char(field, dataset.dicts[field]))

            # elif dct['column'] == field and dct['type'] == 'Boolean':

            #     result.append(get_boolean(field, dataset.dicts[field]))
            # elif dct['column'] == field and dct['type'] == 'Date':

            #     result.append(get_date(field, dataset.dicts[field]))

    return result

with open('input/taylor_swift_spotify.csv', 'r') as infile:
    reader = csv.DictReader(infile, lineterminator='')  
    lst = list(reader)

response = get_type(lst)
print(get_sub_type(response))