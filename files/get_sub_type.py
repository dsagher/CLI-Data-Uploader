from convert import get_type, extract_unique_values, dataset
import csv
from pprint import pprint


def get_boolean(key, values):
    pass

def get_numeric(key: str, value: set):

    '''
    The problem I'm running into right now is that this function is getting looped, causing a few problems. 
    One of them being - I want to ask 'Is this money' to force Numeric, but that question is being asked a bunch 
    of times. So I think I need to collect the list in the main function, and parse through it inside this function.
    Or I should ask this in the main function, even though that kind of splits up the thought. 
    '''
    # Initialize
    dct = dict()
    len_lst = list()
    mx_lst = list()
    mn_lst = list()
    
    # Change value from set to list to iterate
    dct[key] = list(value)
    
    # Generator expressions
    cnt = str(max(len(i) for i in dct[key]))
    mx = max(i for i in dct[key])
    mn = min(i for i in dct[key])
    dec = any('.' in i for i in dct[key])
    # is_money = input('Does this field contain currency? (y/n) ')

    if dec:
        print(f'Use Numeric for {key}')
    elif dec:
        print(f'Use Numeric or Floating Point Precision for {key}')
    else:
        print(f'Use Integer for {key}')
    
    
    return f'length is {cnt}, max is {mx}, min is {mn}, has decimal? {dec}'

    

def get_char(key, values):
    pass

def get_date(key, values):
    pass

def get_sub_type(response: list) -> dict:

    result = dict()

    for dct in response: 
        for field in dataset.columns:
            if dct['column'] == field and dct['type'] == 'Numeric':
                # print('hooray,', dct['column'], 'is a', dct['type'])
                result[field] = get_numeric(field, dataset.dicts[field])

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
pprint(get_sub_type(response))