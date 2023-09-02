#!/usr/bin/env python
"""Small program to transform an image as ASCII art
"""
import argparse
from pathlib import Path

import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
from skimage.transform import resize

CHARACTERS = [" ", " ", " ", ".", ",", ":", "i", "l", "w", "W"]


def main(args: argparse.Namespace):
    """Generate the ascii art

    :param args: CLI user input
    """
    image: np.ndarray = img.imread(args.input_file)
    grey_scale_image: np.ndarray = np.transpose(image.mean(-1))
    if args.invert:
        grey_scale_image: np.ndarray = 1 - grey_scale_image
    grey_scale_image = (
        (len(CHARACTERS) - 1)
        * (grey_scale_image - grey_scale_image.min())
        / (grey_scale_image.max() - grey_scale_image.min())
    )
    x, y = (
        160,
        grey_scale_image.shape[1] * 80 / grey_scale_image.shape[0],
    )
    down_sampled_grey_scale_image: np.ndarray = resize(grey_scale_image, (x, y))
    string = "\n".join(
        [
            "".join(
                [
                    str(CHARACTERS[int(down_sampled_grey_scale_image[i][j])])
                    for i in range(down_sampled_grey_scale_image.shape[0])
                ]
            )
            for j in range(down_sampled_grey_scale_image.shape[1])
        ]
    )
    plt.figure(figsize=(x / 11.1, y / 7.1))
    plt.text(0.5, 0.5, string, family="monospace", ha="center", va="center", fontsize=10, color="#990000")
    plt.axis("off")
    plt.savefig(args.output_file, transparent=True)


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--input-file", type=Path, help="Path to the input image file")
    parser.add_argument(
        "--output-file", type=Path, help="Path to the output image file"
    )
    parser.add_argument(
        "--invert", help="Whether to invert or not", action="store_true"
    )
    main(parser.parse_args())
