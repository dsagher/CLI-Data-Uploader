from convert import get_type, extract_unique_values, dataset
import csv
from pprint import pprint


# will take out later and use only in main()  
with open('input/taylor_swift_spotify.csv', 'r') as infile:
    reader = csv.DictReader(infile, lineterminator='')  
    lst = list(reader)


def get_boolean(key, values):
    pass

def get_numeric(key, value):
    # initialize dct 
    dct = dict()
    # initialize lst
    len_lst = list()
    mx_lst = list()
    mn_lst = list()
    
    # Change value from set to list to iterate
    dct[key] = list(value)
    
    # Generator expression for max str length in each value
    cnt = max(len(i) for i in dct[key])

    # append to len_lst
    len_lst.extend((key, cnt))
    
    # Find max #
    mx = max(i for i in dct[key])

    # add to mx_lst
    mx_lst.extend((key, mx))

    # Find min #
    mn = min(i for i in dct[key])

    # append to min lst 
    mn_lst.extend((key, mn))

    print(len_lst, mx_lst, mn_lst)

def get_char(key, values):
    pass

def get_date(key, values):
    pass

response = get_type(lst)

def get_sub_type(response):

    for dct in response: 
        for field in dataset.columns:
            if dct['column'] == field and dct['type'] == 'Numeric':
                # print('hooray,', dct['column'], 'is a', dct['type'])
                get_numeric(field, dataset.dicts[field])    
            elif dct['column'] == field and dct['type'] == 'Character':
                # print('hooray,', dct['column'], 'is a', dct['type'])
                get_char(field, dataset.dicts[field])
            elif dct['column'] == field and dct['type'] == 'Boolean':
                # print('hooray,', dct['column'], 'is a', dct['type'])
                get_boolean(field, dataset.dicts[field])
            elif dct['column'] == field and dct['type'] == 'Date':
                # print('hooray,', dct['column'], 'is a', dct['type'])
                get_date(field, dataset.dicts[field])

get_sub_type(response)
# print(response)