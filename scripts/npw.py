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
        with gr.Accordion("NPW", open=False, elem_id="#npw"):                                              
            z_weight = gr.Slider(minimum=0, maximum=2.0, step=.01, value=1, label="Negative Prompt Weight")

        self.infotext_fields = []        
        self.infotext_fields.extend([
            (z_weight, "NPW_weight"),
        ])
        self.paste_field_names = []
        for _, field_name in self.infotext_fields:
            self.paste_field_names.append(field_name)
        return [z_weight]
    

    def process(self, p, z_weight):    

        z_weight = getattr(p, 'NPW_weight', z_weight) 
        self.weight = z_weight
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
        new_uncond = torch.lerp(self.empty_uncond, uncond, self.weight)
        params.text_uncond = new_uncond

    def make_empty_uncond(self):
        empty_uncond = shared.sd_model.get_learned_conditioning([""])
        return empty_uncond

def xyz_support():
    for scriptDataTuple in scripts.scripts_data:
        if os.path.basename(scriptDataTuple.path) == 'xyz_grid.py':
            xy_grid = scriptDataTuple.module

            z_weight = xy_grid.AxisOption(
                '[NPW] Weight',
                float,
                xy_grid.apply_field('NPW_weight')
            )
            xy_grid.axis_options.extend([
                z_weight
            ])
try:
    xyz_support()
except Exception as e:
    print(f'Error trying to add XYZ plot options for Latentshop', e)
