import os
import torch
from diffusers import StableVideoDiffusionPipeline
#from diffusers.utils import export_to_video
from PIL import Image
from .ffmpeg import frames_to_video

model_path = "/home/nd/ai/stable-video-diffusion-img2vid-xt"
video_pipe=None


def generate_video(image_path, output_file, seed=42, decode_chunk_size=8, motion_bucket_id=10, noise_aug_strength=0.1, fps=8):
    global video_pipe
    # Check if model path exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path does not exist: {model_path}")

    # Check if image file exists
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file does not exist: {image_path}")
    
    # Load the model
    try:
        if video_pipe==None:
            video_pipe = StableVideoDiffusionPipeline.from_pretrained(
                model_path, torch_dtype=torch.float16, variant="fp16"
            )
            video_pipe.enable_model_cpu_offload()

    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

    # Load the conditioning image using PIL
    try:
        image = Image.open(image_path)
        image = image.resize((1024, 576))
    except Exception as e:
        raise RuntimeError(f"Failed to load or process image: {e}")

    # Generate the video
    try:
        generator = torch.manual_seed(seed)
        frames = video_pipe(
            image, 
            decode_chunk_size=decode_chunk_size, 
            generator=generator, 
            motion_bucket_id=motion_bucket_id, 
            noise_aug_strength=noise_aug_strength
        ).frames[0]
        frames_to_video(frames, output_file, fps=fps)

    except Exception as e:
        raise RuntimeError(f"Failed to generate video: {e}")

    print(f"Video successfully generated: {output_file}")
