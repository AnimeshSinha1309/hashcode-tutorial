import numpy as np
import tqdm

import collections
import random

import utils

TRIES_VERTICAL_MATCH = 1000
TRIES_HORIZONTAL_MATCH = 1000

random.seed(42)  # reproducible runs

input_files = ["a_example", "b_lovely_landscapes", "c_memorable_moments", "d_pet_pictures", "e_shiny_selfies"]


def convert_to_graph(tag_data):
    adjacency = [[] for _ in range(len(tag_data))]
    find_tag = collections.defaultdict(lambda: [])
    for idx, image_tags in enumerate(tag_data):
        for tag in image_tags:
            find_tag[tag].append(idx)
    for key, value in find_tag.items():
        if len(value) == 2:
            if value[0] > value[1]:
                value[1], value[0] = value[0], value[1]
            adjacency[value[0]].append(value[1])
            adjacency[value[1]].append(value[0])
    return adjacency


def _dfs(root, used, adjacency):
    result = [root]
    while True:
        used[root] = True
        choices = [el for el in adjacency[root] if not used[el]]
        if len(choices) == 0:
            return result
        root = random.choice(choices)
        result.append(root)


def _path(used, adjacency):
    available = [el for el in range(len(adjacency)) if not used[el]]
    root = np.random.choice(available)
    path_1 = _dfs(root, used, adjacency)
    path_2 = _dfs(root, used, adjacency)
    path_1.reverse()
    return path_1[:-1] + path_2


def solve(adjacency):
    used = np.full(shape=len(adjacency), fill_value=False)
    solution = []
    with tqdm.tqdm(total=len(adjacency)) as progress:
        while not np.all(used):
            path = _path(used, adjacency)
            solution.extend(path)
            progress.update(len(path))
    return solution


if __name__ == "__main__":
    filename = input_files[1]
    alignments, tags = utils.read_input(filename)
    graph = convert_to_graph(tags)
    adj_size = list(map(len, graph))
    print(max(adj_size), min(adj_size), sum(adj_size) / len(adj_size))
    solution = solve(graph)
    print("Total Score for %s: %s" % (filename, utils.score(filename, solution)))
    utils.submit(filename, solution)
