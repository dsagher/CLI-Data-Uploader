from convert import get_type, dataset
import csv
from pprint import pprint


def get_boolean(key, values):
    pass

def get_numeric(key: str, value: set) -> str:

    '''
    The problem I'm running into right now is that this function is getting looped, causing a few problems. 
    One of them being - I want to ask 'Is this money' to force Numeric, but that question is being asked a bunch 
    of times. So I think I need to collect the list in the main function, and parse through it inside this function.
    Or I should ask this in the main function, even though that kind of splits up the thought. 
    '''
    # Initialize
    dct = dict()
    lst = list()
    
    # Change value from set to list to iterate
    dct[key] = list(value)
    
    # Generator expressions
    cnt = str(max(len(i) for i in dct[key]))
    mx = max(i for i in dct[key])
    mn = min(i for i in dct[key])
    dec = any('.' in i for i in dct[key])
    precise = ''
    
    if dec:
        for i in dct[key]:
            left, right = i.split('.')
            cnt_left = len(left)
            cnt_right = len(right)
            
    # is_money = input('Does this field contain currency? (y/n) ')
    # Could ask "which columns should contain precise precision?"

    if dec and precise:
        result = f'{key} NUMERIC'
    elif dec and not precise and cnt <= '6':
        result = f'{key} REAL'
    elif dec and not precise and cnt <= '15':
        result = f'{key} DOUBLE PRECISION'
    elif not dec and '-32768' <= mn and mx <= '32767':
        result = f'{key} SMALLINT'
    elif not dec and '-2147483648' <= mn and mx <= '2147483647':
        result = f'{key} INT'
    elif not dec and '-9223372036854775808' <= mn and mx <= '9223372036854775807':
        result = f'{key} BIGINT'
    else:
        result = f'Unknown for: {key}'
    
    return result
    # return f'length is {cnt}, max is {mx}, min is {mn}, has decimal? {dec}'

    

def get_char(key, values):
    pass

def get_date(key, values):
    pass

def get_sub_type(response: list) -> list:

    result = list()

    for dct in response: 
        for field in dataset.columns:
            if dct['column'] == field and dct['type'] == 'Numeric':
                # print('hooray,', dct['column'], 'is a', dct['type'])
                result.append(get_numeric(field, dataset.dicts[field]))

            # elif dct['column'] == field and dct['type'] == 'Character':
            #     # print('hooray,', dct['column'], 'is a', dct['type'])
            #     result[field] = get_char(field, dataset.dicts[field])
            # elif dct['column'] == field and dct['type'] == 'Boolean':
            #     # print('hooray,', dct['column'], 'is a', dct['type'])
            #     result[field] = get_boolean(field, dataset.dicts[field])
            # elif dct['column'] == field and dct['type'] == 'Date':
            #     # print('hooray,', dct['column'], 'is a', dct['type'])
            #     result[field] = get_date(field, dataset.dicts[field])

    return result

with open('input/taylor_swift_spotify.csv', 'r') as infile:
    reader = csv.DictReader(infile, lineterminator='')  
    lst = list(reader)

response = get_type(lst)
print(get_sub_type(response))