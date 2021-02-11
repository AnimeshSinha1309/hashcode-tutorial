import random
import typing
import utils

TRIES_VERTICAL_MATCH = 1000
TRIES_HORIZONTAL_MATCH = 1000

random.seed(42)  # reproducible runs

input_files = ["a_example", "b_lovely_landscapes", "c_memorable_moments", "d_pet_pictures", "e_shiny_selfies"]

def separate_horizontal_vertical(alignment_values):
    horizontal_image_idx, vertical_image_idx = list(), list()
    for idx, alignment in enumerate(alignment_values):
        if alignment == 'H':
            horizontal_image_idx.append(idx)
        elif alignment == 'V':
            vertical_image_idx.append(idx)
    return horizontal_image_idx, vertical_image_idx


def greedy_match_vertical(vertical_image_idx, tag_data):
    # mutable reference used later
    slideshow_slides: typing.List[typing.Union[typing.Tuple[int, int], int]] = []

    # Combine the Vertical Images
    while len(vertical_image_idx) >= 2:
        chosen_element = random.choice(vertical_image_idx)
        vertical_image_idx.remove(chosen_element)
        chosen_match, match_score = None, -100000
        for _ in range(TRIES_VERTICAL_MATCH):
            trying_match = random.choice(vertical_image_idx)
            trying_score = utils.overlap_size(tag_data, chosen_element, trying_match)
            if trying_score > match_score:
                match_score = trying_score
                chosen_match = trying_match
        slideshow_slides.append((chosen_element, chosen_match))
        vertical_image_idx.remove(chosen_match)

    return slideshow_slides


def greedy_arrange_slides(slideshow_slides, tag_data):
    # Arrange all the images
    solution_array = [random.choice(slideshow_slides)]
    slideshow_slides.remove(solution_array[0])

    while len(slideshow_slides) >= 1:
        chosen_element = solution_array[-1]
        chosen_match, match_score = None, -100000
        for _ in range(TRIES_HORIZONTAL_MATCH):
            trying_match = random.choice(slideshow_slides)
            trying_score = utils.slide_score(tag_data, chosen_element, trying_match)
            if trying_score > match_score:
                match_score = trying_score
                chosen_match = trying_match
        solution_array.append(chosen_match)
        slideshow_slides.remove(chosen_match)
    return solution_array


if __name__ == "__main__":
    filename = input_files[2]
    alignments, tags = utils.read_input(filename)
    horizontal_images, vertical_images = separate_horizontal_vertical(alignments)
    slides = greedy_match_vertical(vertical_images, tags) + horizontal_images
    solution = greedy_arrange_slides(slides, tags)
    print("Total Score for %s: %s" % (filename, utils.score(filename, solution)))
    utils.submit(filename, solution)
