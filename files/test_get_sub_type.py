from get_sub_type import (get_char, 
                          get_date, 
                          get_numeric)
from pytest import raises
from main import main

def test_get_date():
    assert get_date('column_name', {'02-19-1995'}) == 'column_name DATE'
    assert get_date('column_name', {'02/19/1995'}) == 'column_name DATE'
    assert get_date('column_name', {'1995/02/19'}) == 'column_name DATE'
    assert get_date('column_name', {'1995-02-19'}) == 'column_name DATE'
    assert get_date('column_name', {'19-02-1995'}) == 'column_name DATE'
    assert get_date('column_name', {'19/02/1995'}) == 'column_name DATE'
    assert get_date('column_name', {'1995/02/19 01:23:45'}) == 'column_name TIMESTAMP'
    assert get_date('column_name', {'1995-02-19 01:23:45'}) == 'column_name TIMESTAMP'
    assert get_date('column_name', {'01:23:45'}) == 'column_name TIME'

    with raises(ValueError, match=r'column_name Inconsistent Format: Date: 1995-02-19 Time: NA Timestamp: 02-19-1995 01:23:45'):
        get_date('column_name', {'1995-02-19', '02-19-1995 01:23:45'})
    
    with raises(ValueError, match=r'column_name Inconsistent Format: Date: 02-19|20-1995 Time: 01:23:45 Timestamp: NA'):
        get_date('column_name', {'01:23:45', '02-19-1995', '02-20-1995'})

    with raises(ValueError, match=r'column_name Unknown Format: 1995/02'):
        get_date('column_name', {'1995/02'})
    
    with raises(ValueError, match=r'column_name DATE Incorrect Format: 1995'):
        get_date('column_name', {'1995-02-19', '1995'})

    with raises(ValueError, match=r'column_name Inconsistent Format: Date: NA Time: 01:23:45 Timestamp: 02-19-1995 01:23:45'):
        get_date('column_name', {'01:23:45', '02-19-1995 01:23:45'})

def test_get_char():
    assert get_char('column_name', {'hello', 'good', 'bye'}) == 'column_name VARCHAR'
    assert get_char('column_name', {'hey','bye','hii'}) == 'column_name CHAR(3)'
    assert get_char('column_name', {'hi there', '123', '///'}) == 'column_name VARCHAR'

    text1 = '*' * 65536
    text2 = '_' * 65537
    assert get_char('column_name', {text1, text2}) == 'column_name TEXT'
    assert get_char('column_name', {'123', '123', '123'}) != 'column_name VARCHAR' or 'column_name TEXT' or 'column_name CHAR(3)'

def test_get_numeric():
    assert get_numeric('column_name', {'-123', '456', '789'}, []) == 'column_name SMALLINT'
    assert get_numeric('column_name', {'-2147483647', '2147483646'}, []) == 'column_name INT'
    assert get_numeric('column_name', {'-9223372036854775807', '44556677','9223372036854775806'}, []) == 'column_name BIGINT'
    assert get_numeric('column_name', {'1.234','5.678'}, ['column_name']) == 'column_name NUMERIC'
    assert get_numeric('column_name', {'1.234','5.678'}, []) == 'column_name REAL'
    assert get_numeric('column_name', {'1.234567','5.678912345'}, []) == 'column_name DOUBLE PRECISION'
    assert get_numeric('column_name', {'1.234567','5.678912345'}, ['column_name']) == 'column_name NUMERIC'