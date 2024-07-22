import argparse
import os

'''
This file will provide code for command line functionality 
with help features and descriptions

'''
print(os.stat('demo.txt'))
directory = os.path.abspath('files/arg.py')

def parse():
    parser = argparse.ArgumentParser(description="Convert a dataset to SQL DDL and upload to PostgreSQL.")
    parser.add_argument('--host', default='localhost', type=str, help='Database host.')
    parser.add_argument('--port', default=5432, type=int, help='Database port.')
    return parser.parse_args()

    
file = input('What is the file path? ')
# summary = input('Would you like a summary? ')























# okay = '%*#'

# table = Table(title ='Star Wars Movies')
# table.add_column('poopy', style='magenta')
# table.add_row('Dec 69, 1969')
# console = Console()
# console.print(table)

# custom_theme = Theme({'success':'green', 'error':'bold red'})
# console = Console(theme=custom_theme)
# console.print('Success', style = 'success')

# console.print(':thumbs_up: :apple:')

# console.print('[italic]hello[/] world', style='bold underline red on white')

# text = Text('Hello, World')
# text.stylize('bold magenta', 0, 6)
# console.print(text)

# def add(x, y):
#     a = 'hello'
#     console.log('adding two numbers.', log_locals = True)
#     return x+y 

# console = Console()

# add(1, 2)
# add(1, 3)
# add(1,'a')

