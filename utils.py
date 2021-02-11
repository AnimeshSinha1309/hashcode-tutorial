import os
import sys
import random


def set_seed():
    seed = sys.argv[1] if len(sys.argv) > 1 else 42
    random.seed(seed)  # reproducible runs


def read_input(filename):
    filename = "input/" + filename + ".txt"
    alignment, tags = [], []
    with open(filename, 'r') as f:
        _n = int(f.readline())
        for line in f.readlines():
            data = list(line.strip().split())
            alignment.append(data[0])
            tags.append(set(data[2:]))
    return alignment, tags


def score(filename, solution):
    alignment, tags = read_input(filename)
    points = 0
    for slide in solution:
        if type(slide) is int:
            assert alignment[slide] == 'H'
        elif type(slide) is tuple:
            assert len(slide) == 2
            assert alignment[slide[0]] == 'V' and alignment[slide[1]] == 'V'
    for i in range(1, len(solution)):
        u, v = solution[i - 1], solution[i]
        points += slide_score(tags, u, v)
    return points


def slide_score(tags, u, v):
    x = tags[u] if type(u) is int else \
        tags[u[0]] | tags[u[1]]
    y = tags[v] if type(v) is int else \
        tags[v[0]] | tags[v[1]]
    overlap = len(x & y)
    return min(overlap, len(x) - overlap, len(y) - overlap)


def overlap_size(tags, u, v):
    return len(tags[u] | tags[v])


def submit(filename, solution):
    os.makedirs("output", exist_ok=True)
    filename = "output/" + filename + ".txt"
    with open(filename, 'w') as f:
        f.write(str(len(solution)) + "\n")
        for item in solution:
            if type(item) is int:
                f.write(str(item) + "\n")
            else:
                f.write(str(item[0]) + " " + str(item[1]) + "\n")
