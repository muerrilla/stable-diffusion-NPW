import os
import torch
import gradio as gr

import modules.scripts as scripts
import modules.shared as shared
from modules.script_callbacks import CFGDenoiserParams, on_cfg_denoiser, remove_current_script_callbacks


class Script(scripts.Script):

    def title(self):
        return "Negative Prompt Weight Extention"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion("Negative Prompt Weight", open=True, elem_id="npw"):                                                          
            with gr.Row(equal_height=True):
                with gr.Column(scale=100):
                    weight_input_slider = gr.Slider(minimum=0.00, maximum=2.00, step=.05, value=1.00, label="Weight", interactive=True, elem_id="npw-slider")
                with gr.Column(scale=1, min_width=120):
                    with gr.Row():
                        weight_input = gr.Number(value=1.00, precision=4, label="Negative Prompt Weight", show_label=False, elem_id="npw-number")   
                        reset_but = gr.Button(value='✕', elem_id='npw-x', size='sm')        

            js = """(v) => {
              ['#tab_txt2img #npw-x', '#tab_img2img #npw-x'].forEach((selector, index) => {
                const element = document.querySelector(selector);
                if (document.querySelector(`#tab_${index ? 'img2img' : 'txt2img'}`).style.display === 'block') {
                  element.style.cssText += `outline:4px solid rgba(255,186,0,${Math.sqrt(Math.abs(v-1))}); border-radius: 0.4em !important;`;
                }
              });
              return v;
            }"""
               
            weight_input.change(None, [weight_input], weight_input_slider, _js=js)
            weight_input_slider.change(None, weight_input_slider, weight_input, _js="(x) => x")
            reset_but.click(None, [], [weight_input,weight_input_slider], _js="(x) => [1,1]")


        self.infotext_fields = []        
        self.infotext_fields.extend([
            (weight_input, "NPW_weight"),
        ])
        self.paste_field_names = []
        for _, field_name in self.infotext_fields:
            self.paste_field_names.append(field_name)

        return [weight_input]
    

    def process(self, p, weight):    

        weight = getattr(p, 'NPW_weight', weight) 
        if weight != 1 : self.print_warning(weight)
        self.weight = weight
        self.empty_uncond = None      
        

        if hasattr(self, 'callbacks_added'):
            remove_current_script_callbacks()
            delattr(self, 'callbacks_added')
            # print('NPW callback removed')  

        if self.weight != 1.0:
            self.empty_uncond = self.make_empty_uncond() 
            on_cfg_denoiser(self.denoiser_callback)
            # print('NPW callback added')
            self.callbacks_added = True    

            p.extra_generation_params.update({
                "NPW_weight": self.weight,
            })

        return

    def postprocess(self, p, processed, *args):
        if hasattr(self, 'callbacks_added'):
            remove_current_script_callbacks()
            # print('NPW callback removed in post')

    def denoiser_callback(self, params):
        uncond = params.text_uncond

        if uncond.shape[1] > self.empty_uncond.shape[1]:
            num_concatenations = uncond.shape[1] // self.empty_uncond.shape[1]
            empty_uncond_concat = torch.cat([self.empty_uncond] * num_concatenations, dim=1)
            if uncond.shape[1] == empty_uncond_concat.shape[1] + 1:
                # assuming it's controlnet's marks!
                empty_uncond_concat = torch.cat([uncond[:, :1, :], empty_uncond_concat], dim=1)
            new_uncond = torch.lerp(empty_uncond_concat, uncond, self.weight)
        else:
            new_uncond = torch.lerp(self.empty_uncond, uncond, self.weight)
            
        params.text_uncond = new_uncond

    def make_empty_uncond(self):
        empty_uncond = shared.sd_model.get_learned_conditioning([""])
        return empty_uncond

    def print_warning(self, value):
        if value == 1:
            return
        color_code = '\033[33m'  
        if value < 0.5 or value > 1.5:
            color_code = '\033[93m'  
        print(f"\n{color_code}ATTENTION: Negative prompt weight is set to {value}\033[0m")


def xyz_support():
    for scriptDataTuple in scripts.scripts_data:
        if os.path.basename(scriptDataTuple.path) == 'xyz_grid.py':
            xy_grid = scriptDataTuple.module

            npw_weight = xy_grid.AxisOption(
                '[NPW] Weight',
                float,
                xy_grid.apply_field('NPW_weight')
            )
            xy_grid.axis_options.extend([
                npw_weight
            ])
try:
    xyz_support()
except Exception as e:
    print(f'Error trying to add XYZ plot options for NPW', e)
