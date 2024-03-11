from pprint import pprint
import random
import math

TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


def generate_stamp(previous_value: dict) -> dict:
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = 1 if score_changed and random.random() > 1 - \
        PROBABILITY_HOME_SCORE else 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


def generate_game() -> list[dict]:
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


game_stamps = generate_game()
pprint(game_stamps)


def get_score(game_stamps: list[dict], offset: int):

    if offset < 0 or offset >= len(game_stamps):
        low, high = 0, len(game_stamps) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_offset = game_stamps[mid]["offset"]
            if mid_offset == offset:
                # Нашли точное совпадение смещения
                return game_stamps[mid]["score"]["home"], game_stamps[mid]["score"]["away"]
            elif mid_offset < offset:
                low = mid + 1
            else:
                high = mid - 1

        if high < 0:
            return 0, 0
        else:
            return game_stamps[high]["score"]["home"], game_stamps[high]["score"]["away"]

