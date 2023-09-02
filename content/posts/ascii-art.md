---
title: "Generating ASCII-art"
date: 2023-08-19T12:25:00+02:00
draft: false
short: '<a href="https://en.wikipedia.org/wiki/The_Little_Prince">The little Prince:</a> "If you please, draw me a sheep!" <br> Computer: "1100111010"<br> <a href="https://en.wikipedia.org/wiki/The_Little_Prince">The little Prince:</a> "That is exactly what I wanted!"'
tags: [cli, python, ascii]
img: /ascii-art.png
---

This post is mostly an excuse for me to "document" the code that generates the thumbnails of this website, (and also to remember how I did it).
Without further ado, let's dive into it.

## Requirements

![](/ascii-art-picture.png)

I want a simple program that transforms a image into it's ASCII art equivalent:
- The program should be short
- The program should be easy to modify
- The program should accept the different popular imaging formats (PNG, JPG, JPEG...)
- The program should produce light images (below 200kB)
- I should be able interact with the program through a command line interface (CLI)

Now, I know what I need let's go for it :)

## Ascii art in a nutshell

![](/ascii-art-explanation.png)

The idea of ASCII art, is rather simple:

- Take a list of ASCII characters, and rank them from the less filled to the most filled as follow " ", ".", ",", ":", "i", "l", "w", "W"
- Divide your image in chunks of equal size
- Average the Red / Green / Blue values within a chunck to get the grey value of the chunck
- Replace the chunck with the corresponding character in the list

Simple idea but as we will see in the next section there are some subtility to take into account.

## Implementation

I will not detail entirely the [python script](https://github.com/RobinCamarasa/RobinCamarasa.github.io/blob/master/ascii_art.py) because both you and I have better things to do. I will just highlight the few points that deserve attention.

### Requirements

I tried to keep the requirements list rather short and simple:
- [argparse](https://docs.python.org/3/library/argparse.html) to handle the command line interface
- [numpy](https://numpy.org/) for simple array manipulations
- [matplotlib](https://matplotlib.org/) for the plotting
- [scikit-image](https://scikit-image.org/) for basic image transforms

### Rescaling the image

In the second point _(divide your image in chunks of equal size)_ the size of the of the chunck matters and should match the shape of a letter bounding box.
In my case, I figured that chunks twice higher than wide could do the job just fine.
To make the ASCII art less sensible to the resolution of the input image, I made sure the that the ASCII art would have exactly 160 characters per line and chose the number of line that conserved the original image shape.

The is summed is python as the following snippet of code:

```python
x, y = (
    160,
    grey_scale_image.shape[1] * 80 / grey_scale_image.shape[0],
)
down_sampled_grey_scale_image: np.ndarray = resize(
    grey_scale_image,
    (x, y),
)
```

_Side note: Writing those line I realize that could have checked the actual bounding box size of the font I used, instead of guessing it's ratio but well it works :)_

### Choice of the font

Unfortunately, you cannot any font you want to generate ASCII art.
It is important that the bounding box of all characters of the font you chose have the same size.
In typography, this property is called **monospace**.
I leave below a list of some famous monospaced fonts and as you can see some big hits cannot be used (Times New Roman, Arial...).
In my case, for convenience, I use *Ubuntu mono* but really any would do.

- **monospace:** Courier/Courier New Consolas, Monaco, Lucida Console, Inconsolata, Ubuntu mono...
- **non-monospace:** Times New Roman, Arial, Helvetica, Verdana, Georgia, Palatino...
