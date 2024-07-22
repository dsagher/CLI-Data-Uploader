from convert import get_type, extract_unique_values, dataset
import csv
from pprint import pprint


# will take out later and use only in main()  
with open('input/taylor_swift_spotify.csv', 'r') as infile:
    reader = csv.DictReader(infile, lineterminator='')  
    lst = list(reader)



def get_boolean(values):
    pass

def get_numeric(values):
    pass

def get_char(values):
    pass

def get_date(values):
    pass

response = get_type(lst)


for dct in response:
    for field in dataset.columns:
        if dct['column'] == field and dct['type'] == 'Numeric':
            print('hooray,', dct['column'], 'is a', dct['type'])
            # get_numeric(dataset.values)
        elif dct['column'] == field and dct['type'] == 'Character':
            print('hooray,', dct['column'], 'is a', dct['type'])
            # get_char()
        elif dct['column'] == field and dct['type'] == 'Boolean':
            print('hooray,', dct['column'], 'is a', dct['type'])
            # get_boolean
        elif dct['column'] == field and dct['type'] == 'Date':
            print('hooray,', dct['column'], 'is a', dct['type'])
            # get_date()
