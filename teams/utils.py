from datetime import datetime
from teams.exceptions import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError,
)


def data_processing(data):
    titles = data.get("titles")
    first_cup = data.get("first_cup")
    first_cup_year = int(first_cup[:4])

    if titles < 0:
        raise NegativeTitlesError("titles cannot be negative")

    if first_cup_year < 1930 or (first_cup_year - 1930) % 4 != 0:
        raise InvalidYearCupError("there was no world cup this year")

    max_titles = (datetime.now().year - first_cup_year) // 4 + 1
    if titles > max_titles:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")

    return data
