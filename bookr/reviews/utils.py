from typing import Sequence


def average_rating(rating_list: Sequence) -> float:
    if not rating_list:
        return 0.0

    return round(sum(rating_list) / len(rating_list))
