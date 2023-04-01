
# Negative Prompt Weight

This is a simple extension for the [Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which adds provides a weight parameter for the negative prompt. Supports PNGinfo and XYZ Plot.
![An example plot showing the effect of different weights](/assets/example1.jpg "Negative Prompt: Male")
![Another example plot showing the effect of different weights](/assets/example2.jpg "Negative Prompt: Female")

## Usage

After installing, you can find the new slider called "Negative Prompt Weight" in the scripts sectionm under NPW. 

![Screenshot of the slider provided by the extension in UI](/assets/scr.png "Does what it says on the box.")


## Installation
For now, clone this repo in your extensions folder, or manually create a folder in there and call it what you want, then copy the `scripts` folder of this repo in there.

## How It's Done

At runtime a new learned conditioning `empty_uncond` is made from an empty prompt. Then at every step, inside the denoiser callback, the scheduled `uncond` of the denoiser (which is based on whatever prompt hijinks were passed to the parser) is lerped with the `empty_uncond`.

## Comparisons and Stuff
...soon