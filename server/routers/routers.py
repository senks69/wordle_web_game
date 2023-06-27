import os

from fastapi import APIRouter
from pydantic import BaseModel

from secrets import token_hex

from functions.db_functions import (
        write_new_room, 
        get_game_document, 
        write_word,
        update_game_status,
        clear_room
    )
from functions.words_functions import is_allowed_to_add, get_word

class Word_data(BaseModel):
    token: str
    word: str
class Token(BaseModel):
    token: str

router = APIRouter()

@router.get("/create_room")
async def create_room():
    token = token_hex(16)
    word = get_word()
    write_new_room(token, word)
    return token

@router.get("/retry_game")
async def retry_game(token: str):
    # room_data = get_game_document(token.token)
    new_word = get_word()
    clear_room(token, new_word)
    return {
        "message": {
            "text": "Игра началась!",
            "type": "success"
        }
    }

@router.post("/get_room_data")
async def get_room_data(token: Token):
    room_data = get_game_document(token.token)
    if room_data is not None:
        return {
            "game_status": room_data["game_status"],
            "words": room_data["entered_words"]
        }
    else:
        write_new_room(token.token, get_word())
        return {
            "game_status": "not finished",
            "words": []
        }

@router.post("/add_word")
async def send_word(data: Word_data):
    game_document = get_game_document(data.token)
    status = is_allowed_to_add(game_document, data.word)
    if status["permission"]:
        response = write_word(data.token, data.word)
    else:
        response = {"word": []}
    if not(status.get("message") is None):
        response["message"] = status.get("message")
    update_game_status(data.token, status.get("game_status"))
    response["game_status"] = status.get("game_status")
    return response