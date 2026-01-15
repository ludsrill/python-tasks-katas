from fastapi import APIRouter
from pydantic import BaseModel

from app.katas.dictionary import Dictionary

router = APIRouter()

dictionary_instance = Dictionary()


class DictionaryEntry(BaseModel):
    word: str
    definition: str


class DictionaryLookup(BaseModel):
    word: str


@router.post("/newentry")
def new_entry(entry: DictionaryEntry):
    dictionary_instance.newentry(entry.word, entry.definition)
    return {
        "message": "Entry added successfully",
        "word": entry.word,
        "definition": entry.definition,
    }


@router.get("/look/{word}")
def look_word(word: str):
    result = dictionary_instance.look(word)
    return {"word": word, "result": result}


@router.post("/look")
def look_word_post(lookup: DictionaryLookup):
    result = dictionary_instance.look(lookup.word)
    return {"word": lookup.word, "result": result}


@router.get("/entries")
def get_all_entries():
    return {
        "entries": dictionary_instance.entries,
        "count": len(dictionary_instance.entries),
    }
