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
app = Blueprint('scenes', __name__)

@app.route('/view_scenes')
def view_scenes():
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes() or []
    return render_template('view_scenes.html', scenes=scenes)

