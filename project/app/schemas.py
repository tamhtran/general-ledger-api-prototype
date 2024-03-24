from pydantic import BaseModel
from decimal import Decimal
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import Account, Region


class BalanceSchema(BaseModel):
    balance: Decimal

AccountSchema = pydantic_model_creator(Account)
RegionSchema = pydantic_model_creator(Region)