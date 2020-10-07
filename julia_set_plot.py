"""Generate an image of the julia set."""

import time, argparse, os, multiprocessing

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

parser.add_argument('--num-frames',
    help="How many frames do you want in the animation?",
    action='store', type=int, default=20)

parser.add_argument('--framerate',
    help="What frame rate do you want for the animation?",
    action='store', type=int, default=5)

parser.add_argument('--num-processes',
    help="How many processes to use with --parallel?",
    action='store', type=int, default=2)

args = parser.parse_args()


# Bounds and critical values
a_bound, b_bound = 1.8, 1.8
escape_bound = 2


def get_iterations(point, c):
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


def get_julia_points(c):
    """Get the number of iterations for each point.
    Returns a list of rows."""
    point_iterations = []
    for a in np.linspace(-a_bound, a_bound, args.num_steps):
        row = []
        for b in np.linspace(-b_bound, b_bound, args.num_steps):
            point = complex(a, b)
            num_iterations = get_iterations(point, c)
            row.append(num_iterations / args.max_iterations)

        point_iterations.append(row)

    return point_iterations


def generate_julia_image(args_list):
    """Generate an image of the julia set."""
    plot_num, c = args_list
    point_iterations = get_julia_points(c)
    
    colors = plt.cm.viridis(point_iterations)*255
    colors = np.array(colors, dtype=np.uint8)
    new_image = PIL.Image.fromarray(colors)

    filename = f"output/animation_files/julia_plot_{plot_num}.png"
    new_image.save(filename)
    print(f"Wrote file: {filename}")


def get_plot_nums_c_vals(c_imag_increment):
    """Return a set of c values for a fractal animation.
    c values range from c(a, b) to c(a, b+c_imag_increment),
      where a and b are the initial components of c.

    We want one c-value for every frame in the animation.
    Return a dict of form {'00001': complex}
      The keys will be used in the filename, to make sure image files are
      processed in the correct order for the animation.
    """
    c_initial = complex(-0.62772, -0.42193)
    c_imag_max = c_initial.imag + c_imag_increment
    c_dict = {}
    for plot_num, c_imag in enumerate(
            np.linspace(c_initial.imag, c_imag_max, args.num_frames)):
        key = f"{plot_num:05}"
        new_c = complex(c_initial.real, c_imag)
        c_dict[key] = new_c

    return c_dict


def generate_images():
    """Generate a sequence of images to make an animation."""
    plot_nums_c_vals = get_plot_nums_c_vals(1.5)

    # Clear previously-generated animation output files.
    os.system('rm -rf output/animation_files')
    os.system('mkdir -p output/animation_files')

    # Generate image files in parallel.
    args_list = [(plot_num, c) for plot_num, c in plot_nums_c_vals.items()]
    pool = multiprocessing.Pool(processes=args.num_processes)
    pool.map(generate_julia_image, args_list)


def generate_animation():
    """Process image files to generate an animation."""
    os.system(f"cd output/animation_files && ffmpeg -framerate {args.framerate} -pattern_type glob -i '*.png'   -c:v libx264 -pix_fmt yuv420p julia_animation.mp4")


if __name__ == '__main__':
    start = time.perf_counter()

    generate_images()
    generated_images = time.perf_counter()

    # Generate animation.
    generate_animation()
    generated_animation = time.perf_counter()

    # Summarize execution time:
    image_generation_time = round(generated_images - start, 1)
    animation_generation_time = round(generated_animation - generated_images, 1)
    total_time = round(generated_animation - start, 1)

    print(f"\nGenerated {args.num_frames} image files.")
    print(f"num_steps: {args.num_steps}")
    print(f"max_iterations: {args.max_iterations}")

    print(f"Spent {image_generation_time} seconds generating images.")
    print(f"Spent {animation_generation_time} seconds generating animation.")
    print(f"Spent {total_time} seconds in total.")