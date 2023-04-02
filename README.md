
# Negative Prompt Weight

This is a simple extension for the [Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which provides a weight parameter for the negative prompt.

![Another example plot showing the effect of different weights](/assets/example1.jpg)
*Negative Prompt: Male*

![Another example plot showing the effect of different weights](/assets/example2.jpg)
*Negative Prompt: Female*

Oh, and it writes the value to PNGinfo and supports XYZ Plot.

## Usage

After installing, you can find the new slider called "Negative Prompt Weight" in the scripts section under NPW. 

![Screenshot of the slider provided by the extension in UI](/assets/scr.png "Does what it says on the box.")


## Installation

For now, clone this repo in your extensions folder, or manually create a folder in there and call it what you want, then copy the `scripts` folder of this repo in there.

## How It's Done

At runtime a new learned conditioning `empty_uncond` is made from an empty prompt. Then at every step, inside the denoiser callback, the scheduled `uncond` of the denoiser (which is based on whatever prompt hijinks were passed to the parser) is lerped with the `empty_uncond`.

## Comparisons and Stuff

Here are some comparisons of NPW with attention/emphasis. So top row is NPW and ottom row is using the (Negative Prompt: 0), (Negative Prompt: 0.25), etc. syntax.

```Prompts: a close up portrait of a cyberpunk [knight|lobster], [lobster| ] armour, cyberpunk!, fantasy, elegant, digital painting, artstation, concept art, matte, sharp focus, art by josan gonzalez```

```Params: Steps: 30, Sampler: DPM++ 2M Karras, CFG scale: 10, Seed: 6, Size: 512x640, Model: deliberate_v2```


![a close up portrait of a cyberpunk knight-2-red](https://user-images.githubusercontent.com/48160881/229320416-c805642e-168d-4d35-a4c8-a1f0b066a982.jpg)
*Negative Prompt: red*



![a close up portrait of a cyberpunk knight-25-samurai pink cg](https://user-images.githubusercontent.com/48160881/229320590-1beaf1ac-5ede-49ad-b2bd-7e761fdd49df.jpg)
*Negative Prompt: samurai pink cg*



![a close up portrait of a cyberpunk knight-42](https://user-images.githubusercontent.com/48160881/229321419-055bd6ad-2931-4ad1-96d2-69b047ea1c97.jpg)
*Negative Prompt: *custom TI embedding**
