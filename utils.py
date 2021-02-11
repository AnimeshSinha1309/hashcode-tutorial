import os
import sys
import random

input_files = ["a_example", "b_lovely_landscapes", "c_memorable_moments", "d_pet_pictures", "e_shiny_selfies"]


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


def solution_loader(filename):
    output_file = f"output/{filename}.txt"
    with open(output_file, "r") as f:
        n = int(f.readline())
        solution = []
        for _ in range(n):
            s = f.readline().split(" ")
            if len(s) == 1:
                solution.append(int(s[0]))
            else:
                solution.append((int(s[0]), int(s[1])))
    return solution


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
    x = tags[u] if type(u) is not tuple else \
        tags[u[0]] | tags[u[1]]
    y = tags[v] if type(v) is not tuple else \
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
            if type(item) is tuple:
                f.write(str(item[0]) + " " + str(item[1]) + "\n")
            else:
                f.write(str(item) + "\n")
