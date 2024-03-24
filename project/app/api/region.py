from fastapi import APIRouter, Path, HTTPException
from app.api import crud
from app.schemas import RegionSchema
from typing import List

router = APIRouter()


@router.get("/", response_model=List[RegionSchema])
async def read_all_regions() -> List[RegionSchema]:
    return await crud.get_all_region()


@router.get("/{id}", response_model=RegionSchema)
async def read_region_by_id(id: int = Path(..., gt=0)) -> RegionSchema:
    region = await crud.get_region_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region