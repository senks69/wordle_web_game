import random
import json


with open("./functions/all_words.json", encoding='utf-8') as file:
    all_words = json.load(file)


def get_word():
    return random.choice(all_words)


def is_word_exist(word):
    return word in all_words

def convert_word(word, main_word, word_number) -> dict[str, list[dict[str, str]]]:
    proccessed_letters = []
    letters = []
    for index, letter in enumerate(word):
        if letter == main_word[index]:
            color = "green"
            proccessed_letters.append(letter)
        elif letter in main_word:
            color = "yellow"
            proccessed_letters.append(letter)
            if (letter in proccessed_letters and 
                main_word.count(letter) < proccessed_letters.count(letter)):
                color = "gray"
                proccessed_letters.remove(letter)
        else:
            color = "gray"
        data = {
            "letter": letter,
            "color": color,
            "position": word_number*5+index
        }
        letters.append(data)
    return {
        'word': letters
    }

def convert_word(word, main_word, word_number) -> dict[str, list[dict[str, str]]]:
    proccessed_letters = []
    letters = []
    for index, letter in enumerate(word):
        if letter == main_word[index]:
            color = "green"
            proccessed_letters.append(letter)
        else:
            color = "gray"
        data = {
            "letter": letter,
            "color": color,
            "position": word_number*5+index
        }
        letters.append(data)
    for index, letter in enumerate(letters):
        if (letter["letter"] in main_word and letter["color"] != "green" and 
            main_word.count(letter["letter"]) > proccessed_letters.count(
                letter["letter"]
            )):
            letters[index]["color"] = "yellow"
            proccessed_letters.append(letter["letter"])
    return {
        'word': letters
    }

def is_allowed_to_add(game_document, word):
    if word == game_document["main_word"]:
        return {
            "message": {
                "text": "Вы выиграли!",
                "type": "success"
            },
            "permission": True,
            "game_status": "Win"
        }
    past_words = game_document["full_words"]
    if word != game_document["main_word"] and len(past_words)>=5:
        return {
            "message": {
                "text": "Вы проиграли.\n" + 
                f"загаданное слово - {game_document['main_word']}",
                "type": "error"
            },
            "permission": True,
            "game_status": "Lose"
        }
    if word in past_words:
        return {
            "message": {
                "text": "Это слово уже было",
                "type": "error"
            },
            "game_status": "not finished",
            "permission": False
        }
    if word not in all_words:
        return {
            "message": {
                "text": "Такого слова не существует...",
                "type": "error"
            },
            "permission": False,
            "game_status": "not finished"
        }
    return {"game_status": "not finished", "permission": True}
