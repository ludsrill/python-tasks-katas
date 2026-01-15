from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.katas.substring import nth_char

router = APIRouter()


class SubstringRequest(BaseModel):
    words: List[str]


@router.post("/nth_char")
def get_nth_char(request: SubstringRequest):
    if not request.words:
        raise HTTPException(
            status_code=400, detail="Words list cannot be empty"
        )

    result = nth_char(request.words)
    return {"input": request.words, "result": result}


@router.get("/nth_char")
def get_nth_char_get(words: str):
    word_list = [w.strip() for w in words.split(",") if w.strip()]
    if not word_list:
        raise HTTPException(
            status_code=400, detail="Words list cannot be empty"
        )

    result = nth_char(word_list)
    return {"input": word_list, "result": result}
