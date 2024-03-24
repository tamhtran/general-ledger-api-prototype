from app.models import Region,  Account
from typing import List, Union
import logging
log = logging.getLogger("uvicorn")

async def get_all_account() -> List:
    accounts = await Account.all().values()
    return accounts


async def get_account_by_id(id: int) -> Union[Account, None]:
    account = await Account.filter(account_id=id).first().values()
    if account:
        return account
    return None


async def get_all_region() -> List:
    regions = await Region.all().values()
    return regions


async def get_region_by_id(id: int) -> Union[Region, None]:
    region = await Region.filter(region_id=id).first().values()
    if region:
        return region
    return None