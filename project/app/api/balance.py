
from fastapi import APIRouter, HTTPException, Query, Path
from app.utils import calculate_balance, parse_date
from app.api import crud
from app.schemas import BalanceSchema

router = APIRouter()
@router.get('/{account_id}/{date}', response_model=BalanceSchema, status_code=201)
async def get_balance(
    account_id: int = Path(
        ...,
        gt=0,
        description="Unique identifier of the account. Must be greater than 0."
    ),
    date: str = Path(
        ...,
        description="The date for which the balance is requested, in a date YYYY-MM-DD format or named date format YYYYQQ such as 2022Q1 or Q1."
    ),
    region_id: int = Query(
        None,
        description="Optional region identifier. If provided, the balance will be calculated for transactions in this region."
    )
) -> BalanceSchema:
    try:
        parsed_date = parse_date(date)
        if not parsed_date:
            raise HTTPException(status_code=403, detail="Date not valid")

        check_account_id = await crud.get_account_by_id(account_id)
        if not check_account_id:
            raise HTTPException(status_code=404, detail="Account not found")
        if region_id is not None:
            check_region_id = await crud.get_region_by_id(region_id)
            if not check_region_id:
                raise HTTPException(status_code=405, detail="Region not found")

        balance = await calculate_balance(account_id, parsed_date, region_id)

        if balance == -999999999999:
            raise HTTPException(status_code=406, detail="Balance not found")

        return {'balance': balance}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
