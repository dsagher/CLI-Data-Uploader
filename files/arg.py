import argparse


'''
This file will provide code for command line functionality 
with help features and descriptions

'''

def parse():
    parser = argparse.ArgumentParser(description="Convert a dataset to SQL DDL and upload to PostgreSQL.")
    parser.add_argument('--host', default='localhost', type=str, help='Database host.')
    parser.add_argument('--port', default=5432, type=int, help='Database port.')
    return parser.parse_args()

    
# summary = input('Would you like a summary? ')


file = input('What is the file path? ')