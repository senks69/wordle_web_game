from pymongo import MongoClient
from functions.words_functions import convert_word

client = MongoClient('mongodb://localhost:27017')
db = client.wordle_data
collection = db.games_data


def write_new_room(token, main_word):
    document = {
        "token": token,
        "main_word": main_word,
        "game_status": "not finished",
        "words_count": 0,
        "full_words":[],
        "entered_words": []
    }
    collection.insert_one(document)

def get_game_document(token):
    return collection.find_one({"token": token})

def write_word(token, word):
    document = get_game_document(token)
    main_word = document["main_word"]
    words_count = document["words_count"]
    converted_word = convert_word(word, main_word, words_count)
    collection.update_one(
        {'token': token}, 
        {
            '$push': {
                'full_words': word
            }
        }
    )
    collection.update_one(
        {'token': token}, 
        {
            '$push': {
                'entered_words': converted_word
            }
        }
    )
    collection.update_one(
        {'token': token}, 
        {'$set': {'words_count': words_count+1}}
    )
    return converted_word

def update_game_status(token, status):
    collection.update_one(
        {'token': token}, 
        {'$set': {'game_status': status}}
    )

def clear_room(token, word):
    result = collection.update_one(
        {'token': token},
        {
            '$set': {
                'main_word': word,
                'game_status': 'not finished',
                'words_count': 0,
                'full_words': [],
                'entered_words': []
            }
        }
    )