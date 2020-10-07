"""Generate an image of the julia set."""

import time, argparse

import numpy as np
from matplotlib import pyplot as plt


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
    """Define the points, and the number of iterations for each point."""
    points, point_iterations = [], []
    for a in np.linspace(-a_bound, a_bound, args.num_steps):
        for b in np.linspace(-b_bound, b_bound, args.num_steps):
            point = complex(a, b)
            iterations = get_iterations(point)
            points.append(point)
            point_iterations.append(iterations)

    return (points, point_iterations)


def plot_julia_points(points, point_iterations):
    # Plot set.
    x_values = [p.real for p in points]
    y_values = [p.imag for p in points]

    plt.style.use('classic')
    fig, ax = plt.subplots(figsize=(14, 10))

    ax.scatter(x_values, y_values, c=point_iterations, cmap=plt.cm.viridis,
            edgecolors='none', s=4)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    filename = f"output/julia_plot_mpl-{args.num_steps}-maxiter-{args.max_iterations}.png"
    plt.savefig(filename)


if __name__ == '__main__':
    start = time.perf_counter()

    points, point_iterations = get_julia_points()
    generated_points = time.perf_counter()

    plot_julia_points(points, point_iterations)
    generated_plot = time.perf_counter()

    # Summarize execution time:
    analysis_time = round(generated_points - start, 1)
    plotting_time = round(generated_plot - generated_points, 1)
    total_time = round(generated_plot - start, 1)

    print(f"num_steps: {args.num_steps}")
    print(f"max_iterations: {args.max_iterations}")

    print(f"\nSpent {analysis_time} seconds generating julia points.")
    print(f"Spent {plotting_time} seconds generating plot.")
    print(f"Spent {total_time} seconds in total.")