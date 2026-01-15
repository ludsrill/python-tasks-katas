from typing import Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.katas.spending import get_total_cost

router = APIRouter()


class SpendingRequest(BaseModel):
    items: Dict[str, float]


@router.post("/total")
def calculate_total(request: SpendingRequest):
    if not request.items:
        raise HTTPException(
            status_code=400, detail="Items dictionary cannot be empty"
        )

    total = get_total_cost(request.items)
    return {
        "items": request.items,
        "total": total,
        "item_count": len(request.items),
    }
