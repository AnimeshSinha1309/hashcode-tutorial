import utils
import random

utils.set_seed()

input_files = ["a_example", "b_lovely_landscapes", "c_memorable_moments", "d_pet_pictures", "e_shiny_selfies"]

filename = input_files[2]
alignments, tags = utils.read_input(filename)

horizontal_images, vertical_images = [], []

for idx, alignment in enumerate(alignments):
    if alignment == 'H':
        horizontal_images.append(idx)
    elif alignment == 'V':
        vertical_images.append(idx)

TRIES_VERTICAL_MATCH = 50
TRIES_VERTICAL_SLIDE_MATCH = 1000

# list of slides of either two V photos or one H photos EACH
solution = []
iterations = 0
mod = 5

while vertical_images or horizontal_images:
    previous_slide = solution[-1] if solution else None

    if iterations % mod == mod - 1:
        print(iterations, len(vertical_images), len(horizontal_images))
    iterations += 1

    best_slide_score, best_slide = -1, None
    if vertical_images:
        # select best next vertical image pair
        for __ in range(TRIES_VERTICAL_SLIDE_MATCH):
            chosen_v = random.choice(vertical_images)

            best_score, match_v = -1, None
            for _ in range(TRIES_VERTICAL_MATCH):
                next_v = random.choice(vertical_images)
                if next_v == chosen_v:
                    continue

                curr_score = utils.overlap_size(tags, chosen_v, next_v)
                if curr_score > best_score:
                    best_score = curr_score
                    match_v = next_v

            if match_v is None:
                continue
            # select best next slide:
            slide_curr = (chosen_v, match_v)
            if previous_slide:
                slide_curr_score = utils.slide_score(tags, previous_slide, slide_curr)
            else:
                slide_curr_score = best_score

            if slide_curr_score > best_slide_score:
                best_slide = slide_curr
                best_slide_score = slide_curr_score

    best_score, match_h = -1, None
    if horizontal_images:
        for image in horizontal_images:
            if previous_slide:
                curr_score = utils.slide_score(tags, previous_slide, image)
            else:
                curr_score = len(tags[image])

            if curr_score > best_score:
                best_score = curr_score
                match_h = image

    if best_score > best_slide_score:
        solution.append(match_h)
        horizontal_images.remove(match_h)
    else:
        solution.append(best_slide)
        vertical_images.remove(best_slide[0])
        vertical_images.remove(best_slide[1])

print("Total Score for %s: %s" % (filename, utils.score(filename, solution)))
utils.submit(filename, solution)
