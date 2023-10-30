
# Negative Prompt Weight

This is a simple extension for the [Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which allows users to adjust the overall weight of the negative prompt, allowing you to increase or decrease its effect in a new way. Oh, and it writes the value to PNGinfo, honors it during 'send to txt2img' etc., and supports XYZ Plot.

## What Does It Do?

Here's a demonstration of how it can continously reduce the effect of the negative prompt from what you normally get (on the right, with weight 1.0) to nothing, as if the negative prompt was empty (on the left, with weight 0.0):

![Another example plot showing the effect of different weights](/assets/example1.jpg)
*Prompt: portrait of zimby anton fadeev cyborg propaganda poster*<br>
*Params: Steps: 30, Sampler: DPM++ SDE Karras, CFG scale: 7.5, Seed: 918, Size: 512x640, Model: deliberate_v2* <br>
*Negative Prompt: Male*

![Another example plot showing the effect of different weights](/assets/example2.jpg)
*Prompt: portrait of zimby anton fadeev cyborg propaganda poster*<br>
*Params: Steps: 30, Sampler: DPM++ SDE Karras, CFG scale: 7.5, Seed: 918, Size: 512x640, Model: deliberate_v2* <br>
*Negative Prompt: Female*

### Why Use This?

This method was originally intended for <b>decreasing</b> the effect of the negative prompt, which is very hard or at times impossible to do with the currently available methods like Better Prompting™, Attention/Emphasis (using the '(prompt:weight)' syntax), Prompt Editing (using the [prompt1:prompt2:when] syntax), etc. But you can also use it with values higher than 1 and it will boost your negative prompt in its own style (you might need to lower your CFG scale a bit if you do that).

Here is the first example compared to using the '(negative prompts: weight)' syntax (i.e. bottom row is (negative prompt:0),(negative prompt:0.25),etc.:

![portrait of zimby anton fadeev cyborg propaganda poster-24-male](https://user-images.githubusercontent.com/48160881/229344713-81793753-d9ae-4927-b5e9-03a7749dfc95.jpg)

Please have a look at the examples in the [comparisons](https://github.com/muerrilla/stable-diffusion-NPW#more-comparisons-and-stuff) section if you want to know how it's different from using '(prompt:weight)' and check out the discussion [here](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/9220) if you need more context.

## Installation

Open SD WebUI > Go to Extensions tab > Go to Available > Press the big button > Find 'Negative Prompt Weight' in the list > Click Install

Or manually clone this repo into your extensions folder:

`git clone "https://github.com/muerrilla/stable-diffusion-NPW" extensions/stable-diffusion-NPW`

## Usage

![Screenshot of the slider provided by the extension in UI](/assets/screenshot.png "Does what it says on the box.")

After installing, you can locate the new parameter "Negative Prompt Weight" in the extentions area of txt2img and img2img tabs. 

## Limitations

Doesn't work with SDXL yet.

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

## How It's Done

At runtime a new learned conditioning tensor `empty_uncond` is made from an empty prompt. Then at every step, inside the denoiser callback, the scheduled `uncond` tensor of the denoiser (which is based on whatever prompt hijinks were passed to the parser) is lerped with the `empty_uncond` to weaken it's effect. The lerp function can instead be given a parameter bigger than 1, and it will boost the effect of the negative prompt like the CFG scale does for the positive.
