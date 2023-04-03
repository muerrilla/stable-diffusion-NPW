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
        with gr.Accordion("Negative Prompt Weight", open=False, elem_id="npw"):                                              
            with gr.Row(equal_height=True):
                with gr.Column(scale=100):
                    ui_feedback = gr.Checkbox(value=True, interactive=True, label="UI Feedback")
                with gr.Column(scale=1, min_width=84):
                    weight_input = gr.Number(value=1.0, precision=3, label="Negative Prompt Weight", show_label=False)            

            dummy = gr.Checkbox(visible=False)  
            js = """(v, d) => {
                let t=document.querySelector('#txt2img_negative_token_counter'),
                    i=document.querySelector('#img2img_negative_token_counter');
                t.style.cssText+=`outline:4px solid rgba(255,0,128,${d*Math.sqrt(Math.abs(v-1))}); border-radius: 0.4em !important;`
                i.style.cssText+=`outline:4px solid rgba(255,0,128,${d*Math.sqrt(Math.abs(v-1))}); border-radius: 0.4em !important;`
                }"""                                      
            weight_input.change(None, [weight_input, ui_feedback], dummy, _js=js)
            ui_feedback.change(None, [weight_input, ui_feedback], dummy, _js=js)

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
    print(f'Error trying to add XYZ plot options for Latentshop', e)
