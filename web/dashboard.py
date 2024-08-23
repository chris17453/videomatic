import os
import sys
import re
import json
import mimetypes
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, Response,jsonify, Blueprint


# Get the path to the 'web' directory
web_dir = os.path.dirname(os.path.abspath(__file__))

# Get the path to the project root (parent of 'web')
project_root = os.path.dirname(web_dir)

# Add the project root to the Python path
sys.path.append(project_root)

# Path to the data directory (sibling of 'web')
data_dir = os.path.join(project_root, "data")


from videomatic.scene import Scene
from videomatic.video import make_scenes
from videomatic.flux import flux_image
from videomatic.svd import generate_video
from videomatic.queue import connect_to_db, add_to_queue, get_queue_status
from videomatic.ffmpeg import get_video_length


# Create a Blueprint
# Create a Blueprint
app = Blueprint('dashboard', __name__)

@app.route('/')
def index():
    # Step 1: Retrieve scenes
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes() or []
    num_scenes = len(scenes)
    
    # Step 2: Check if the final video is built
    video_path = scene.video['final']
    video_exists = os.path.exists(video_path)  # Check if the video file exists

    if video_exists:
        # Step 3: Get video length if it exists
        video_length = get_video_length(video_path)  # Assuming you have this function
        video_status = f"Length: {video_length} seconds."
    else:
        video_status = "Video not built"
    print(scene)
    is_synced=scene.is_synced()
    
    # Step 4: Render this information in your homepage template
    return render_template('homepage.html', num_scenes=num_scenes, video_status=video_status, video_exists=video_exists,is_synced=is_synced)

