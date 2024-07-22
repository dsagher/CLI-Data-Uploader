import pytest
from convert import get_type, extract_unique_values



def test_char():
    lst_of_dicts = [{'hello':'123'}, {'goodbye':'456'}]
    assert get_type(lst_of_dicts) != [{'column': 'hello', 'type': 'Character'}]

    lst_of_dicts = [{'hello':'abc'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Character'}]

    lst_of_dicts = [{'hello':'ab3'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Character'}]

    lst_of_dicts = [{'hello':'/(abc)/123'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Character'}]

    lst_of_dicts = [{'hello':'true'}]
    assert get_type(lst_of_dicts) != [{'column': 'hello', 'type': 'Character'}]

    lst_of_dicts = [{'hello':'True'}]
    assert get_type(lst_of_dicts) != [{'column': 'hello', 'type': 'Character'}]

    lst_of_dicts = [{'hello':'TRUE'}]
    assert get_type(lst_of_dicts) != [{'column': 'hello', 'type': 'Character'}]

    lst_of_dicts = [{'hello':'false'}]
    assert get_type(lst_of_dicts) != [{'column': 'hello', 'type': 'Character'}]

    lst_of_dicts = [{'hello':'False'}]
    assert get_type(lst_of_dicts) != [{'column': 'hello', 'type': 'Character'}]

    lst_of_dicts = [{'hello':'FALSE'}]
    assert get_type(lst_of_dicts) != [{'column': 'hello', 'type': 'Character'}]


def test_numeric():
    lst_of_dicts = [{'hello':'123'}, {'goodbye':'456'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Numeric'}]

    lst_of_dicts = [{'hello':'4bbe3'}]
    assert get_type(lst_of_dicts) != [{'column': 'hello', 'type': 'Numeric'}]

    lst_of_dicts = [{'hello':'1.23'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Numeric'}]

    lst_of_dicts = [{'hello':'.23'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Numeric'}]

    lst_of_dicts = [{'hello':'1112341.235432123'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Numeric'}]

    lst_of_dicts = [{'hello':'!23'}]
    assert get_type(lst_of_dicts) != [{'column': 'hello', 'type': 'Numeric'}]

    lst_of_dicts = [{'hello':'1'}, {'hello':'0'}]
    assert get_type(lst_of_dicts) != [{'column': 'hello', 'type': 'Numeric'}]
    

def test_date():

    lst_of_dicts = [{'hello': '1995-02-19'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Date'}]

    lst_of_dicts = [{'hello': '02-19-1995'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Date'}]

    lst_of_dicts = [{'hello': '19-02-1995'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Date'}]

    lst_of_dicts = [{'hello': '19-2-1995'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Date'}]

    lst_of_dicts = [{'hello': '2-19-1995'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Date'}]


def test_bool():
    
    lst_of_dicts = [{'hello':'True'},{'hello':'False'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Boolean'}]

    lst_of_dicts = [{'hello':'1'}, {'hello':'0'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Boolean'}]

    lst_of_dicts = [{'hello':'true'},{'hello':'false'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Boolean'}]

    lst_of_dicts = [{'hello':'TRUE'},{'hello':'FALSE'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Boolean'}]

    lst_of_dicts = [{'hello':'t'},{'hello':'F'}]
    assert get_type(lst_of_dicts) == [{'column': 'hello', 'type': 'Boolean'}]

def test_extract_unique_values():

    lst_of_dicts = [{'hello':'1'},{'hello':'0'},{'hello':'1'},{'hello':'0'}]
    assert extract_unique_values(lst_of_dicts) == {'hello'}

    lst_of_dicts = [{'hello':'1'},{'hello':'0'},{'hey':'1'},{'hey':'1'}, {'who':'3'}]
    assert extract_unique_values(lst_of_dicts) == {'hello','hey'}

    


