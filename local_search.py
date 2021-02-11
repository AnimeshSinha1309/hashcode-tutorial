import numpy as np

import utils


def _score_element(solution, tags, idx, neighborhood):
    total_score = 0
    if neighborhood > 0:
        total_score += utils.slide_score(solution[neighborhood - 1], solution[idx], tags)
    if neighborhood + 1 < len(solution):
        total_score += utils.slide_score(solution[idx], solution[neighborhood + 1], tags)
    return total_score


def _score_pair(solution, tags, u, v):
    return _score_element(solution, tags, u, v) + _score_element(solution, tags, v, u) - \
           _score_element(solution, tags, u, u) - _score_element(solution, tags, u, v)
