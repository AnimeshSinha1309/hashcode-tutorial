import utils
import random

import tqdm

import greedy_graph


utils.set_seed()

input_files = ["a_example", "b_lovely_landscapes", "c_memorable_moments", "d_pet_pictures", "e_shiny_selfies"]

TRIES_VERTICAL_MATCH = 50
TRIES_VERTICAL_SLIDE_MATCH = 1000


def online_arrange_slides(horizontal_image_idx, vertical_image_idx, tag_data):
    # list of slides of either two V photos or one H photos EACH
    result = []

    total_slides, current_slides = len(vertical_image_idx) // 2 + len(horizontal_image_idx), 0
    progress_bar = tqdm.tqdm(total=total_slides)

    while vertical_image_idx or horizontal_image_idx:
        previous_slide = result[-1] if result else None

        best_slide_score, best_slide = -1, None
        if vertical_image_idx:
            # select best next vertical image pair
            for __ in range(TRIES_VERTICAL_SLIDE_MATCH):
                chosen_v = random.choice(vertical_image_idx)
                best_score, match_v = -1, None
                for _ in range(TRIES_VERTICAL_MATCH):
                    next_v = random.choice(vertical_image_idx)
                    if next_v != chosen_v:
                        curr_score = utils.overlap_size(tag_data, chosen_v, next_v)
                        if curr_score > best_score:
                            best_score = curr_score
                            match_v = next_v

                if match_v is None:
                    continue
                # select best next slide:
                slide_curr = (chosen_v, match_v)
                slide_curr_score = utils.slide_score(tag_data, previous_slide, slide_curr) \
                    if previous_slide else best_score
                if slide_curr_score > best_slide_score:
                    best_slide = slide_curr
                    best_slide_score = slide_curr_score

        best_score, match_h = -1, None
        if horizontal_image_idx:
            for image in horizontal_image_idx:
                curr_score = utils.slide_score(tag_data, previous_slide, image) \
                    if previous_slide else len(tag_data[image])
                if curr_score > best_score:
                    best_score = curr_score
                    match_h = image

        if best_score > best_slide_score:
            result.append(match_h)
            horizontal_image_idx.remove(match_h)
        else:
            result.append(best_slide)
            vertical_image_idx.remove(best_slide[0])
            vertical_image_idx.remove(best_slide[1])
        current_slides += 1
        progress_bar.update(current_slides)

    progress_bar.close()
    return result


if __name__ == "__main__":
    filename = input_files[2]
    alignments, tags = utils.read_input(filename)
    horizontal_images, vertical_images = greedy_graph.separate_horizontal_vertical(alignments)
    solution = online_arrange_slides(horizontal_images, vertical_images, tags)
    print("Total Score for %s: %s" % (filename, utils.score(filename, solution)))
    utils.submit(filename, solution)
