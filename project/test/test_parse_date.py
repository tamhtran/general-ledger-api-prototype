from app.utils import parse_date
from datetime import datetime

def test_parse_regular_date():
    assert parse_date("2022-03-31") == datetime(2022, 3, 31)
    assert parse_date("2022/03/31") == datetime(2022, 3, 31)

def test_parse_q1_2022():
    assert parse_date("Q12022") == datetime(2022, 1, 1)

def test_parse_2022_q2():
    assert parse_date("2022Q2") == datetime(2022, 4, 1)

def test_parse_q3_current_year():
    current_year = datetime.now().year
    assert parse_date("Q3") == datetime(current_year, 7, 1)

def test_parse_invalid_date():
    assert parse_date("Not a date") is None
    assert parse_date("Q5") is None
    assert parse_date("2014Q5") is None
    assert parse_date("2022/13/31") is None