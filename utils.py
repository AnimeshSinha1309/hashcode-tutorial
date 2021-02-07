import os


def read_input(file):
    file = "input/" + file + ".txt"
    alignment, tags = [], []
    with open(file, 'r') as f:
        _n = int(f.readline())
        for line in f.readlines():
            data = list(line.strip().split())
            alignment.append(data[0])
            tags.append(data[2:])
    return alignment, tags


def score(file, solution):
    alignment, tags = read_input(file)
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
    x = set(tags[u]) if type(u) is int else \
        set(tags[u[0]]) | set(tags[u[1]])
    y = set(tags[v]) if type(v) is int else \
        set(tags[v[0]]) | set(tags[v[1]])
    overlap = len(x & y)
    return min(overlap, len(x) - overlap, len(y) - overlap)


def overlap_size(tags, u, v):
    x = set(tags[u])
    y = set(tags[v])
    return len(x | y)


def submit(file, solution):
    os.makedirs("output", exist_ok=True)
    file = "output/" + file + ".txt"
    with open(file, 'w') as f:
        f.write(str(len(solution)) + "\n")
        for item in solution:
            if type(item) is int:
                f.write(str(item) + "\n")
            else:
                f.write(str(item[0]) + " " + str(item[1]) + "\n")
