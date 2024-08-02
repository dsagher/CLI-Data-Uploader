from convert import dataset
from re import fullmatch
from typing import Optional

def get_boolean(key: str) -> str:
    '''
    params:
        key - one column name

    output:
        str: 'column BOOLEAN'  
    '''
    
    result = f'{key} BOOLEAN'

    return result
    
def get_numeric(key: str, value: set, precision_decision: list) -> str:
    '''
    params: 
        key - one column name
        value - a set of unique values for that column
        precision_decision - a list of columns that the user specified require precision
    
    output:
        str: 'column_name DATATYPE'

    '''
    dct = dict()
    
    
    dct[key] = list(value)
    
    cnt = max(len(i) for i in dct[key])
    mx = max(i for i in dct[key])
    mn = min(i for i in dct[key])
    dec = any('.' in i for i in dct[key])
    
     
    if dec:
        result = f'{key} NUMERIC' if key in precision_decision else \
                 f'{key} REAL' if cnt <= 6 else \
                 f'{key} DOUBLE PRECISION' if cnt <= 15 else \
                 f'{key} Unknown for: {key}'  # Default to DOUBLE PRECISION if conditions are met

    else:
        int_mn, int_mx = int(mn), int(mx)
        result = f'{key} SMALLINT' if -32768 <= int_mn and int_mx <= 32767 else \
                 f'{key} INT' if -2147483648 <= int_mn and int_mx <= 2147483647 else \
                 f'{key} BIGINT' if -9223372036854775808 <= int_mn and int_mx <= 9223372036854775807 else \
                 f'Unknown for: {key}'
        
    return result

def get_index() -> Optional[str]:
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

    if same:
        result = f'{key} CHAR({lengths[0]})'
    else:
        result = f'{key} VARCHAR' if mx < 65535 else \
                 f'{key} TEXT'

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
        for v in list(values):
            
            if fullmatch(date_pattern_1, v) or fullmatch(date_pattern_2, v):
                date_lst.append(v)

            elif fullmatch(date_pattern_1 + r'\s' + time_pattern, v):
                timestamp_lst.append(v)

            elif fullmatch(time_pattern, v):
                time_lst.append(v)

            else:
                unformatted_lst.append(v)

        # Set result to appropriate DDL statement
        if unformatted_lst: # Recognize incorrect formats
            if date_lst:
                raise ValueError(f'{key} DATE Incorrect format: {unformatted_lst}')
            elif timestamp_lst:
                raise ValueError(f'{key} TIMESTAMP Incorrect format: {unformatted_lst}')
            elif time_lst:
                raise ValueError(f'{key} TIME Incorrect format: {unformatted_lst}')
            else:
                raise ValueError(f'{key} Unknown Format {unformatted_lst}')
        
        elif (date_lst and (time_lst or timestamp_lst)) or (timestamp_lst and time_lst):
            # Recognize correct but inconsistent formats
            raise ValueError(f'{key} Inconsistent format: {date_lst[0] if date_lst else ""} \
                                                          {time_lst[0] if time_lst else ""} \
                                                          {timestamp_lst[0] if timestamp_lst else ""}')
        
        
        # If lsts exists and all the values made it through the conditional 
        elif date_lst and len(date_lst) == len(values): 
            result = f'{key} DATE'
        elif timestamp_lst and len(timestamp_lst) == len(values):
            result = f'{key} TIMESTAMP'
        elif time_lst and len(time_lst) == len(values):
            result = f'{key} TIME'
        else:
            result = f'{key} Unknown Format'                   

    except ValueError as e:
        print(f' Error Occured Processessing a Date Column : {str(e)}')

    return result