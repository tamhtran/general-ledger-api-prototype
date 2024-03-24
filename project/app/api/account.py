from fastapi import APIRouter, Path, HTTPException
from app.api import crud
from app.schemas import AccountSchema
from typing import List

router = APIRouter()


@router.get("/", response_model=List[AccountSchema])
async def read_all_accounts() -> List[AccountSchema]:
    return await crud.get_all_account()


@router.get("/{id}", response_model=AccountSchema)
async def read_account_by_id(id: int = Path(..., gt=0)) -> AccountSchema:
    account = await crud.get_account_by_id(id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account