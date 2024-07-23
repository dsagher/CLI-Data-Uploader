import csv
from convert import del_index, get_type
import argparse
'''

main() will call arg to ask user for file and arguments. 
file will then be passed into:

extract_unique_values() - adds column names and unique values to the DataSet class and returns a list of boolean columns
del_index() -

get_type()- get_type() will return statements of general data type classification to get_sub_type().

get_sub_type() - will determine which subtype to use, and/or ask the user what they want to use based off what options they have.
                results will be passed to generate_ddl()

generate_ddl() - will generate SQL data definition language and pass result to push()

push()- will use SQLalchemy to push to a Postgres server. 

'''


def main():

    file = input('What is the file path? ')

    with open(file, 'r') as infile:
        reader = csv.DictReader(infile, lineterminator='')  
        lst = list(reader)

    get_type(lst)
    lst = del_index(lst)


def parse():
    parser = argparse.ArgumentParser(description="Convert a dataset to SQL DDL and upload to PostgreSQL.")
    parser.add_argument('--host', default='localhost', type=str, help='Database host.')
    parser.add_argument('--port', default=5432, type=int, help='Database port.')
    return parser.parse_args()

    
# summary = input('Would you like a summary? ')

main()