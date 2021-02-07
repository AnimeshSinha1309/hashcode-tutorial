import random

import utils

input_files = ["a_example", "b_lovely_landscapes",
               "c_memorable_moments", "d_pet_pictures", "e_shiny_selfies"]
file = input_files[0]
alignments, tags = utils.read_input(file)

TRIES_VERTICAL_MATCH = 100
TRIES_HORIZONTAL_MATCH = 100


horizontal_images, vertical_images = list(), list()

for idx, alignment in enumerate(alignments):
    if alignment == 'H':
        horizontal_images.append(idx)
    elif alignment == 'V':
        vertical_images.append(idx)

# Combine the Vertical Images

while len(vertical_images) >= 2:
    chosen_element = random.choice(vertical_images)
    vertical_images.remove(chosen_element)
    chosen_match, match_score = None, -100000
    for _ in range(TRIES_VERTICAL_MATCH):
        trying_match = random.choice(vertical_images)
        trying_score = utils.overlap_size(tags, chosen_element, trying_match)
        if trying_score > match_score:
            match_score = trying_score
            chosen_match = trying_match
    horizontal_images.append((chosen_element, chosen_match))
    vertical_images.remove(chosen_match)

# Arrange all the images

solution = [random.choice(horizontal_images)]
horizontal_images.remove(solution[0])

while len(horizontal_images) >= 1:
    chosen_element = solution[-1]
    chosen_match, match_score = None, -100000
    for _ in range(TRIES_HORIZONTAL_MATCH):
        trying_match = random.choice(horizontal_images)
        trying_score = utils.slide_score(tags, chosen_element, trying_match)
        if trying_score > match_score:
            match_score = trying_score
            chosen_match = trying_match
    solution.append(chosen_match)
    horizontal_images.remove(chosen_match)


print("Total Score for %s: %s" % (file, utils.score(file, solution)))
utils.submit(file, solution)
