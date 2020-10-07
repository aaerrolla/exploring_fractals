"""Generate an image of the julia set."""

import numpy as np
from matplotlib import pyplot as plt


# Bounds and critical values
a_bound, b_bound = 1.8, 1.8
c = -0.62772 - 0.42193j
max_iterations = 20
escape_bound = 2
num_steps = 200


def get_iterations(point):
    """How many iterations does it take to exceed the critical value?"""
    iteration = 0
    pv = point**2 + c
    while iteration < max_iterations:
        if abs(pv) > escape_bound:
            return iteration
        else:
            pv = pv**2 + c
            iteration += 1
    return iteration


def get_julia_points():
    """Define the points, and the number of iterations for each point."""
    points, point_iterations = [], []
    for a in np.linspace(-a_bound, a_bound, num_steps):
        for b in np.linspace(-b_bound, b_bound, num_steps):
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

    plt.show()


if __name__ == '__main__':
    points, point_iterations = get_julia_points()
    plot_julia_points(points, point_iterations)