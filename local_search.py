import numpy as np
import tqdm
import copy

import utils


def _score_element(solution, tags, idx, neighborhood):
    total_score = 0
    if neighborhood > 0:
        total_score += utils.slide_score(tags, solution[neighborhood - 1], solution[idx])
    if neighborhood + 1 < len(solution):
        total_score += utils.slide_score(tags, solution[idx], solution[neighborhood + 1])
    return total_score


def _score_swap(solution, tags, u, v):
    if abs(u - v) == 0:
        return 0
    elif abs(u - v) == 1:
        score = 0
        if u > v:
            u, v = v, u
        if u > 0:
            score -= utils.slide_score(tags, solution[u - 1], solution[u])
            score += utils.slide_score(tags, solution[u - 1], solution[v])
        if v + 1 < len(solution):
            score -= utils.slide_score(tags, solution[v], solution[v + 1])
            score += utils.slide_score(tags, solution[u], solution[v + 1])
        return score
    else:
        return _score_element(solution, tags, u, v) + _score_element(solution, tags, v, u) - \
               _score_element(solution, tags, u, u) - _score_element(solution, tags, v, v)


def simulated_annealing(solution, tags, n_iter=1000000):
    temperature = 100
    best_score, best_solution = utils.score(file, solution), solution
    current_score = best_score
    with tqdm.trange(n_iter) as progress:
        for i in progress:
            u = np.random.randint(len(solution))
            v = np.random.randint(len(solution))
            score_delta = _score_swap(solution, tags, u, v)
            prob = 1 if score_delta > 0 else np.exp(score_delta / temperature)
            if np.random.random() < prob:
                solution[u], solution[v] = solution[v], solution[u]
                current_score += score_delta
            if (i + 1) % 100 == 0:
                temperature *= 0.95
            if current_score > best_score:
                best_score = current_score
                best_solution = copy.deepcopy(solution)
            progress.set_postfix(best_score=best_score, current_score=current_score)
    return best_solution


if __name__ == "__main__":
    file = utils.input_files[2]
    alignments, tag_values = utils.read_input(file)
    initial_solution = utils.solution_loader(file)
    print(initial_solution[:100])
    print("Initial Score", utils.score(file, initial_solution))
    final_solution = simulated_annealing(initial_solution, tag_values)
    print("Final Score", utils.score(file, final_solution))
