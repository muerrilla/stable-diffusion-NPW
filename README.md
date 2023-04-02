
# Negative Prompt Weight

This is a simple extension for the [Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which allows users to adjust the weight parameter for the negative prompt.


![Another example plot showing the effect of different weights](/assets/example1.jpg)
*Prompt: portrait of zimby anton fadeev cyborg propaganda poster*<br>
*Params: Steps: 30, Sampler: DPM++ SDE Karras, CFG scale: 7.5, Seed: 918, Size: 512x640, Model: deliberate_v2* <br>
*Negative Prompt: Male*

![Another example plot showing the effect of different weights](/assets/example2.jpg)
*Prompt: portrait of zimby anton fadeev cyborg propaganda poster*<br>
*Params: Steps: 30, Sampler: DPM++ SDE Karras, CFG scale: 7.5, Seed: 918, Size: 512x640, Model: deliberate_v2* <br>
*Negative Prompt: Female*

Here is the first example compared to using the '(negative prompts: weight)' syntax (i.e. bottom row is (negative prompt:0),(negative prompt:0.25),etc.:

![portrait of zimby anton fadeev cyborg propaganda poster-24-male](https://user-images.githubusercontent.com/48160881/229344713-81793753-d9ae-4927-b5e9-03a7749dfc95.jpg)

Oh, and it writes the value to PNGinfo and supports XYZ Plot.

## Usage

After installing, you can locate the new slider called "Negative Prompt Weight" in the scripts section under NPW. 

![Screenshot of the slider provided by the extension in UI](/assets/scr.png "Does what it says on the box.")


## Installation

For now, clone this repo in your extensions folder, or manually create a folder in there and call it what you want, then copy the `scripts` folder of this repo in there.

## How It's Done

At runtime a new learned conditioning `empty_uncond` is made from an empty prompt. Then at every step, inside the denoiser callback, the scheduled `uncond` of the denoiser (which is based on whatever prompt hijinks were passed to the parser) is lerped with the `empty_uncond`.

## More Comparisons and Stuff

Here are some comparisons between NPW and Attention/Emphasis. So, top row is using NPW and bottom row is using the (Negative Prompt: weight) syntax with the same weights.

```Prompts: a close up portrait of a cyberpunk [knight|lobster], [lobster| ] armour, cyberpunk!, fantasy, elegant, digital painting, artstation, concept art, matte, sharp focus, art by josan gonzalez```

```Params: Steps: 30, Sampler: DPM++ 2M Karras, CFG scale: 10, Seed: 6, Size: 512x640, Model: deliberate_v2```


![a close up portrait of a cyberpunk knight-2-red](https://user-images.githubusercontent.com/48160881/229320416-c805642e-168d-4d35-a4c8-a1f0b066a982.jpg)
*Negative Prompt: red*



![a close up portrait of a cyberpunk knight-25-samurai pink cg](https://user-images.githubusercontent.com/48160881/229320590-1beaf1ac-5ede-49ad-b2bd-7e761fdd49df.jpg)
*Negative Prompt: samurai pink cg*



![a close up portrait of a cyberpunk knight-42](https://user-images.githubusercontent.com/48160881/229321419-055bd6ad-2931-4ad1-96d2-69b047ea1c97.jpg)
*Negative Prompt: *custom TI embedding**
