import torch
from diffusers import FluxPipeline

model_path="/home/nd/ai/FLUX.1-schnell"
#model_path="/home/nd/ai/flux-fp8/"
pipe = None



def flux_image(prompt,output_file,guidance=3.5, steps=10,sequence_length=256):
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
        guidance_scale=guidance,
        output_type="pil",
        num_inference_steps=steps,
        max_sequence_length=sequence_length,
        generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]
    image.save(output_file)

