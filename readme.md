Exploring Fractals
===

This is a companion repository to [this post]().

To run the code in this repository:

```
$ git clone [address]
$ cd exploring_fractals
$ python -m venv f_env
$ source f_env/bin/activate
(f_env)$ pip install -r requirements.txt
(f_env)$ python julia_set_plot.py
```

This will generate an animation file in *output/animation_files*.

To see all options:

```
(f_env)$ python julia_set_plot.py --help
```

This program uses parallel processing, and you can adjust how many processes to use with the `--num-processes` flag. Here's a command to generate a high-resolution, smooth animation. This command takes about 10 minutes to render on my moderately specced 13" macbook pro, with 2 processes:

```
(f_env)$ python julia_set_plot.py --max-iterations 500 --framerate 30 --duration 10 --num-steps 500 --c-imag-initial -0.42 --c-imag-increment 0.042
```
