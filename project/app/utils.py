import re
from datetime import datetime
from dateutil import parser

from tortoise.transactions import in_transaction
from decimal import Decimal
import logging

log = logging.getLogger("uvicorn")


def quarter_to_date(quarter_str):
    """
    # Parse a string representing a quarter into a datetime object
    # Examples of valid input: "Q12022", "2022Q2", "Q3", "2022", "Q1", "2022Q1"
    :param quarter_str:
    :return:
    """
    match = re.match(r'(Q[1-4])(\d{4})|(\d{4})(Q[1-4])|(Q[1-4])$', quarter_str, re.IGNORECASE)

    if not match:
        return "Invalid format"

    quarter = (match.group(1) or match.group(4) or match.group(5)).upper()
    year = int(match.group(2) or match.group(3) or datetime.now().year)

    quarters = {
        "Q1": datetime(year, 1, 1),
        "Q2": datetime(year, 4, 1),
        "Q3": datetime(year, 7, 1),
        "Q4": datetime(year, 10, 1)
    }

    return quarters.get(quarter, "Invalid quarter")


def parse_date(date_str) -> datetime:
    """
    parse_date() will attempt to parse a string into a datetime object
    If the string is not recognized as a date, it will attempt to parse it as a quarter
    If the string is not recognized as a quarter, it will return None
    Examples of valid input: "2021-01-01", "2021-1-1", "Q12021", "2021Q1", "Q1", "2021", "Q1 2021"
    :param date_str:
    :return:
    """
    try:
        # Try parsing the date directly
        return parser.parse(date_str)
    except ValueError:
        # If direct parsing fails, try parsing as a quarter
        quarter_date = quarter_to_date(date_str)
        if quarter_date != "Invalid format":
            return quarter_date
    # Return None if neither date nor quarter format is recognized
    return None


async def execute_raw_query(query):
    async with in_transaction() as connection:
        result = await connection.execute_query(query)
        return result

# Calculate the balance for a given account up to a given date
# Optionally, filter by region
# Example usage: calculate_balance(1, datetime.date(2021, 1, 1), 1)
async def calculate_balance(account_id: int, parsed_date: datetime.date, region_id: int = None) -> Decimal:
    # Convert parsed_date to a string in SQL date format
    date_str = parsed_date.strftime('%Y-%m-%d')

    # Construct the base query with joins
    query_join = f"SELECT COALESCE(SUM(t.amount),-999999999999) as balance FROM transactions t "
    query_where = f"WHERE t.account_id = {account_id} AND t.date < '{date_str}' "

    # Add region_id condition if not null
    if region_id is not None:
        query_join += (f"LEFT JOIN countries c ON t.country_id = c.country_id "
                       f"LEFT JOIN regions r ON c.region_id = r.region_id ")
        query_where += f"AND r.region_id = {region_id}"

    query = query_join + query_where
    log.info('INFO: ' + str(query))

    # get the balance from the database
    result = await execute_raw_query(query)
    log.info('INFO: ' + str(result))

    # -999999999999 is the default value for balance if no transactions are found
    if result is None:
        return Decimal(-999999999999)
    else:
        return Decimal(result[1][0]['balance'])
