"""Generate an image of the julia set."""

import time, argparse

import numpy as np
from matplotlib import pyplot as plt
import PIL


# Parse cli arguments.
parser = argparse.ArgumentParser()

parser.add_argument('--num-steps',
    help="How many steps between horizontal and vertical bounds?",
    action='store', type=int, default=200)

parser.add_argument('--max-iterations',
    help="What's the max number of iterations to try on each point?",
    action='store', type=int, default=20)

args = parser.parse_args()


# Bounds and critical values
a_bound, b_bound = 1.8, 1.8
c = -0.62772 - 0.42193j
escape_bound = 2


def get_iterations(point):
    """How many iterations does it take to exceed the critical value?"""
    iteration = 0
    pv = point**2 + c
    while iteration < args.max_iterations:
        if abs(pv) > escape_bound:
            return iteration
        else:
            pv = pv**2 + c
            iteration += 1
    return iteration


def get_julia_points():
    """Get the number of iterations for each point.
    Returns a list of rows."""
    point_iterations = []
    for a in np.linspace(-a_bound, a_bound, args.num_steps):
        row = []
        for b in np.linspace(-b_bound, b_bound, args.num_steps):
            point = complex(a, b)
            num_iterations = get_iterations(point)
            row.append(num_iterations / args.max_iterations)

        point_iterations.append(row)

    return point_iterations


def generate_julia_image(point_iterations):
    """Generate an image of the julia set."""
    
    colors = plt.cm.viridis(point_iterations)*255
    colors = np.array(colors, dtype=np.uint8)
    new_image = PIL.Image.fromarray(colors)

    filename = f"output/julia_plot_pil-{args.num_steps}-maxiter-{args.max_iterations}.png"
    new_image.save(filename)
    print(f"Wrote file: {filename}")


if __name__ == '__main__':
    start = time.perf_counter()

    point_iterations = get_julia_points()
    generated_points = time.perf_counter()

    generate_julia_image(point_iterations)
    generated_image = time.perf_counter()

    # Summarize execution time:
    analysis_time = round(generated_points - start, 1)
    image_generation_time = round(generated_image - generated_points, 1)
    total_time = round(generated_image - start, 1)

    print(f"num_steps: {args.num_steps}")
    print(f"max_iterations: {args.max_iterations}")

    print(f"\nSpent {analysis_time} seconds generating julia points.")
    print(f"Spent {image_generation_time} seconds generating image.")
    print(f"Spent {total_time} seconds in total.")