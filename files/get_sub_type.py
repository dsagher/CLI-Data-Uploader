from convert import dataset
from re import fullmatch


def get_boolean(key: str) -> str:
    '''
    params:
        key - one column name

    output:
        str: 'column BOOLEAN'  
    '''
    
    result = f'{key} BOOLEAN'

    return result
    
def get_numeric(key: str, values: set, precision_decision: list) -> str:
    '''
    params: 
        key - one column name
        value - a set of unique values for that column
        precision_decision - a list of columns that the user specified require precision
    
    output:
        str: 'column_name DATATYPE'

    '''
    # Get rid of nulls for classification
    values = {value for value in values if value.lower() not in ['', 'na', 'null']}

    # Find largest Precision and Scale for each column

    length_lst = set()
    prec_scale = set()

    for value in values:
        if '.' in value:
            length_lst.add(len(value))
            left, right = value.split('.')
            precision = len(left) + len(right)
            scale = len(right)
            prec_scale.add((precision, scale))

    if prec_scale:
        max_precision, max_scale = max(prec_scale, key=lambda x: (x[0], x[1]))

    # Determine specific datatypes - with and without decimals
    dec = any('.' in i for i in values)

    try:
        if dec:

            cnt = max(len(i) for i in values if i != '')

            result = f'{key} NUMERIC({max_precision + 1},{max_scale})' if key in precision_decision \
                    and max_precision is not None and max_scale is not None else \
                    f'{key} REAL' if cnt <= 6 else \
                    f'{key} DOUBLE PRECISION' if cnt <= 15 else \
                    f'{key} NUMERIC' 

        else:

            mx = max(int(i) for i in values if i != '')
            mn = min(int(i) for i in values if i != '')

            result = f'{key} SMALLINT' if -32768 <= mn and mx <= 32767 else \
                    f'{key} INT' if -2147483648 <= mn and mx <= 2147483647 else \
                    f'{key} BIGINT' if -9223372036854775808 <= mn and mx <= 9223372036854775807 else \
                    f'{key} NUMERIC'
    except Exception as e:
        print(f'An error occurred in processing Numeric values:{e}')

    return result

def get_index() -> str:
    '''
    This function runs if user specifies wants index.

    params:
        None
    ouput:
        str: 'index SERIALTYPE'   
    '''

    result =    f'index SMALLSERIAL' if dataset.length <= 32767 else \
                f'index SERIAL' if dataset.length <= 2147483647 else \
                f'index BIGSERIAL' if dataset.length <= 9223372036854775807 else None
    
    return result
        
def get_char(key: str, values: set) -> str:

    '''
    params: 
        key - one column name
        value - a set of unique values for that column
    
    output:
        str: 'columname DATATYPE'

    '''

    mx = max(len(i) for i in values)

    lengths = list(map(lambda x: len(x), values))
    same = all(v == lengths[0] for v in lengths)

    try:
        if same:
            result = f'{key} CHAR({lengths[0]})'
        else:
            result = f'{key} VARCHAR' if mx < 65535 else \
                    f'{key} TEXT'
    except Exception as e:
        print(f'An error occured in processessing Character values:{e}')

    return result

def get_date(key: str, values: set) -> str:
    
    '''
    params: 
        key - one column name
        value - a set of unique values for that column

    output:
        str: 'columnname DATATYPE'

    error:
        raises ValueError if date formats are incorrect or are inconsistent
    '''

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
        for v in values:
            
            if fullmatch(date_pattern_1, v) or fullmatch(date_pattern_2, v):
                date_lst.append(v)

            elif fullmatch(date_pattern_1 + r'\s' + time_pattern, v) or fullmatch(date_pattern_2 + r'\s' + time_pattern, v):
                timestamp_lst.append(v)

            elif fullmatch(time_pattern, v):
                time_lst.append(v)

            elif v.lower() not in ['na', 'null']:
                unformatted_lst.append(v)

        # Raise ValueError for incorrect or inconsistent DATE/TIMESTAMP/TIME
        if unformatted_lst: 
            if date_lst:
                raise ValueError(f'{key} DATE Incorrect Format: {unformatted_lst[0]}')
            elif timestamp_lst:
                raise ValueError(f'{key} TIMESTAMP Incorrect Format: {unformatted_lst[0]}')
            elif time_lst:
                raise ValueError(f'{key} TIME Incorrect Format: {unformatted_lst[0]}')
            else:
                raise ValueError(f'{key} Unknown Format: {unformatted_lst[0]}')
        
        elif (date_lst and (time_lst or timestamp_lst)) or (timestamp_lst and time_lst):
            # Recognize correct but inconsistent formats
            raise ValueError(f'{key} Inconsistent Format: Date: {date_lst[0] if date_lst else "NA"} Time: {time_lst[0] if time_lst else "NA"} Timestamp: {timestamp_lst[0] if timestamp_lst else "NA"}')
        
        
        # If lsts exists and all the values made it through the conditional 
        elif date_lst: 
            result = f'{key} DATE'
        elif timestamp_lst:
            result = f'{key} TIMESTAMP'
        elif time_lst:
            result = f'{key} TIME'
        else:
            result = f'{key} Unknown Format'                   
        return result

    except ValueError as e:
        raise ValueError(e)
