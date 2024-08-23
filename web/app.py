import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, Response,jsonify

from .create_scene import app as create_scene
from .dashboard import app as dashboard
from .scene import app as scene
from .scenes import app as scenes


web_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(web_dir)
sys.path.append(project_root)
data_dir = os.path.join(project_root, "data")



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages


app.register_blueprint(dashboard    ,url_prefix="/") 
app.register_blueprint(create_scene ,url_prefix="/") 
app.register_blueprint(scene        ,url_prefix="/") 
app.register_blueprint(scenes       ,url_prefix="/") 




@app.route('/check_status/<int:scene_id>/<media_type>')
def check_status(scene_id, media_type):
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes()
    
    if scene_id < 1 or scene_id > len(scenes):
        return jsonify({'status': 'error', 'message': 'Invalid scene ID'})
    
    current_scene = scenes[scene_id - 1]
    
    conn = connect_to_db()
    if media_type == 'frame':
        queue_id = current_scene.get('frame', {}).get('queue_id')
    elif media_type == 'video':
        queue_id = current_scene.get('video', {}).get('queue_id')
    else:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Invalid media type'})
    
    status = get_queue_status(conn, queue_id) if queue_id else None
    conn.close()
    
    if status:
        message = f"{media_type.capitalize()} is {status['status']}."
        if status['status'] == 'error':
            message = f"Error generating {media_type}: {status.get('error_message', 'Unknown error')}"
        return jsonify({
            'status': status['status'],
            'message': message
        })
    else:
        return jsonify({'status': 'not_started', 'message': f'{media_type.capitalize()} generation not started'})


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".png": "image/png",
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    print(path)
    
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    print(complete_path,mimetype,ext)
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)



if __name__ == '__main__':
    print(f"Starting application. Data directory: {data_dir}")
    app.run(debug=True)
