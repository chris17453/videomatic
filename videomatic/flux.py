import torch
from diffusers import FluxPipeline

model_path="/home/nd/ai/FLUX.1-schnell"
#model_path="/home/nd/ai/flux-fp8/"
pipe = None



def flux_image(prompt,output_file):
    global pipe
    if pipe==None:
        pipe = FluxPipeline.from_pretrained(model_path, torch_dtype=torch.bfloat16)
        #pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power
        pipe.enable_sequential_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power

    print(prompt)
    

    image = pipe(
        prompt,
        height=576,
        width=1024,
        guidance_scale=2.5,
        output_type="pil",
        num_inference_steps=10,
        max_sequence_length=256,
        generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]
    image.save(output_file)

