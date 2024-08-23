import os
import sys
import re
import json
import mimetypes
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, Response,jsonify, Blueprint
from flask import current_app

web_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(web_dir)
sys.path.append(project_root)
data_dir = os.path.join(project_root, "data")


from videomatic.scene import Scene
from videomatic.video import make_scenes
from videomatic.flux import flux_image
from videomatic.svd import generate_video
from videomatic.queue import connect_to_db, add_to_queue, get_queue_status
from videomatic.ffmpeg import get_video_length


# Create a Blueprint
app = Blueprint('scene', __name__)

@app.route('/scene/<int:scene_id>', methods=['GET', 'POST'])
def view_scene(scene_id):
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes() or []
    
    if scene_id < 1 or scene_id > len(scenes):
        flash('Invalid scene ID', 'error')
        return redirect(url_for('scene.view_scenes'))
    
    current_scene = scenes[scene_id - 1]
    
    if request.method == 'POST':
        # Update scene details
        current_scene['name'] = request.form.get('name', '')
        current_scene['length'] = float(request.form.get('length', 0))
        current_scene['prompt'] = request.form.get('prompt', '')
        current_scene['timestamp'] = float(request.form.get('timestamp', 0))
        
        # Update video parameters
        current_scene['video'] = current_scene.get('video', {})
        current_scene['video']['seed'] = int(request.form.get('video[seed]', 42))
        current_scene['video']['decode_chunk_size'] = int(request.form.get('video[decode_chunk_size]', 8))
        current_scene['video']['motion_bucket_id'] = int(request.form.get('video[motion_bucket_id]', 10))
        current_scene['video']['noise_aug_strength'] = float(request.form.get('video[noise_aug_strength]', 0.1))
        current_scene['video']['fps'] = int(request.form.get('video[fps]', 8))
        
        scene.save()
        flash('Scene updated successfully!', 'success')
        return redirect(url_for('scene.view_scene', scene_id=scene_id))
    
    # Clear messages on page refresh
    if 'frame' in current_scene:
        current_scene['frame'].pop('status_message', None)
    if 'video' in current_scene:
        current_scene['video'].pop('status_message', None)
    
    # Check if frame and video exist
    frame_path = current_scene.get('frame', {}).get('output_path', '')
    video_path = current_scene.get('video', {}).get('output_path', '')
    
    frame_exists = os.path.exists(frame_path) if frame_path else False
    video_exists = os.path.exists(video_path) if video_path else False
    
    # Fetch queue status
    conn = connect_to_db()
    frame_queue_id = current_scene.get('frame', {}).get('queue_id')
    video_queue_id = current_scene.get('video', {}).get('queue_id')
    
    frame_status = get_queue_status(conn, frame_queue_id) if frame_queue_id else None
    video_status = get_queue_status(conn, video_queue_id) if video_queue_id else None
    
    conn.close()
    
    # Prepare status messages
    frame_status_message = get_status_message(frame_status, 'frame', frame_exists)
    video_status_message = get_status_message(video_status, 'video', video_exists)
    
    # Determine if video generation should be allowed
    allow_video_generation = frame_exists and not video_exists
    
    active_tab = request.args.get('active_tab', 'frame')
    
    return render_template('view_scene.html', 
                           scene=current_scene, 
                           scene_id=scene_id, 
                           frame_exists=frame_exists, 
                           video_exists=video_exists,
                           frame_status=frame_status, 
                           video_status=video_status,
                           frame_status_message=frame_status_message,
                           video_status_message=video_status_message,
                           allow_video_generation=allow_video_generation,
                           active_tab=active_tab)

def get_status_message(status, media_type, exists):
    if exists:
        return f""
    elif not status:
        return f"No {media_type} generated yet."
    elif status['status'] == 'pending':
        return f"{media_type.capitalize()} generation is queued."
    elif status['status'] == 'in_progress':
        return f"{media_type.capitalize()} is being generated..."
    elif status['status'] == 'error':
        return f"Error generating {media_type}: {status.get('error_message', 'Unknown error')}"
    #elif status['status'] == 'completed':
    #    return f"{media_type.capitalize()} generated successfully."
    else:
        return f"Unknown status for {media_type}."

@app.route('/scene/<int:scene_id>/delete_frame', methods=['POST'])
def delete_frame(scene_id):
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes() or []
    
    if scene_id < 1 or scene_id > len(scenes):
        flash('Invalid scene ID', 'error')
        return redirect(url_for('scene.view_scenes'))
    
    current_scene = scenes[scene_id - 1]
    frame_path = current_scene.get('frame', {}).get('output_path', '')
    
    if frame_path:
        full_frame_path = os.path.join(data_dir, frame_path)
        if os.path.exists(full_frame_path):
            os.remove(full_frame_path)
            flash('Frame deleted successfully!', 'success')
        else:
            flash('Frame not found', 'error')
    else:
        flash('Frame path not found in scene data', 'error')
    
    # Clear frame status and queue ID
    if 'frame' in current_scene:
        current_scene['frame'].pop('status', None)
        current_scene['frame'].pop('queue_id', None)
    
    scene.save()
    
    return redirect(url_for('scene.view_scene', scene_id=scene_id))

@app.route('/scene/<int:scene_id>/delete_video', methods=['POST'])
def delete_video(scene_id):
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes() or []
    
    if scene_id < 1 or scene_id > len(scenes):
        flash('Invalid scene ID', 'error')
        return redirect(url_for('scene.view_scenes'))
    
    current_scene = scenes[scene_id - 1]
    video_path = current_scene.get('video', {}).get('output_path', '')
    
    if video_path:
        if os.path.exists(video_path):
            os.remove(video_path)
            flash('Video deleted successfully!', 'success')
        else:
            flash('Video file not found', 'error')
    else:
        flash('Video path not found in scene data', 'error')
    
    # Clear video status and queue ID
    if 'video' in current_scene:
        current_scene['video'].pop('status', None)
        current_scene['video'].pop('queue_id', None)
    
    scene.save()
    
    return redirect(url_for('scene.view_scene', scene_id=scene_id))

@app.route('/generate_video')
def generate_video():
    project=Scene(data_dir)
    project.load()
    # this is to generate stuff thats not generated
    project.create_fragments("frames")
    project.create_fragments("video")
    # this is to fix the video lenghts... might change
    project.correct_fragments()
    # This makes the video
    project.build_video()
    flash('Video generation started. This may take a while.', 'info')
    return redirect(url_for('scene.view_scenes'))

@app.route('/frame/<int:scene_id>')
def serve_frame(scene_id):
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes() or []
    
    if scene_id < 1 or scene_id > len(scenes):
        abort(404)
    
    current_scene = scenes[scene_id - 1]
    frame_path = current_scene.get('frame', {}).get('output_path', '')
    
    if frame_path:
        if os.path.exists(frame_path):
            return send_file(frame_path, mimetype='image/png')
    
    abort(404)

@app.route('/video/<int:scene_id>')
def serve_video(scene_id):
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes() or []
    
    if scene_id < 1 or scene_id > len(scenes):
        current_app.logger.error(f"Invalid scene_id: {scene_id}")
        abort(404)
    
    current_scene = scenes[scene_id - 1]
    video_path = current_scene.get('video', {}).get('output_path', '')
    current_app.logger.info(f"Video path from scene data: {video_path}")
    
    if not video_path:
        current_app.logger.error("Video path not found in scene data")
        abort(404)
    
    full_video_path = video_path
    current_app.logger.info(f"Full video path: {full_video_path}")
    
    if not os.path.exists(full_video_path):
        current_app.logger.error(f"Video file does not exist at: {full_video_path}")
        abort(404)
    
    file_size = os.path.getsize(full_video_path)
    current_app.logger.info(f"Video file exists at: {full_video_path}")
    current_app.logger.info(f"File size: {file_size} bytes")

    try:
        response = send_file(full_video_path, mimetype='video/mp4')
        response.headers['Content-Length'] = file_size
        response.headers['Accept-Ranges'] = 'bytes'
        return response
    except Exception as e:
        current_app.logger.error(f"Error serving video: {str(e)}")
        abort(500)


@app.route('/video_final')
def serve_final_video():
    current_app.logger.info(f"Attempting to serve final video")
    
    scene = Scene(data_dir)
    scene.load()
    
    video_path = scene.video.get('final', '')
    current_app.logger.info(f"Video path from final: {video_path}")
    
    if not video_path:
        current_app.logger.error("Video path not found for final")
        abort(404)
    
    full_video_path = video_path
    current_app.logger.info(f"Full video path: {full_video_path}")
    
    if not os.path.exists(full_video_path):
        current_app.logger.error(f"Video file does not exist at: {full_video_path}")
        abort(404)
    
    file_size = os.path.getsize(full_video_path)
    current_app.logger.info(f"Video file exists at: {full_video_path}")
    current_app.logger.info(f"File size: {file_size} bytes")

    try:
        response = send_file(full_video_path, mimetype='video/mp4')
        response.headers['Content-Length'] = file_size
        response.headers['Accept-Ranges'] = 'bytes'
        return response
    except Exception as e:
        current_app.logger.error(f"Error serving video: {str(e)}")
        abort(500)        

@app.route('/video_test/<int:scene_id>')
def video_test(scene_id):
    return render_template('video_test.html', scene_id=scene_id)


@app.route('/download_video/<int:scene_id>')
def download_video(scene_id):
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes() or []
    
    if scene_id < 1 or scene_id > len(scenes):
        abort(404)
    
    current_scene = scenes[scene_id - 1]
    video_path = current_scene.get('video', {}).get('output_path', '')
    
    if not video_path:
        abort(404)
    
    full_video_path = os.path.join(data_dir, video_path)
    
    if not os.path.exists(full_video_path):
        abort(404)
    
    return send_file(full_video_path, as_attachment=True, download_name=f"video_{scene_id}.mp4")

@app.route('/generate_frame/<int:scene_id>', methods=['POST'])
def generate_frame(scene_id):
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes()
    
    if scene_id < 1 or scene_id > len(scenes):
        flash('Invalid scene ID', 'error')
        return redirect(url_for('scene.view_scenes'))
    
    current_scene = scenes[scene_id - 1]
    output_file = current_scene.get('frame', {}).get('output_path')
    
    conn = connect_to_db()
    queue_id = add_to_queue(conn, 1, 'image', {
        'prompt': current_scene['prompt'],
        'output_file': output_file
    })
    conn.close()
    
    current_scene['frame']['queue_id'] = queue_id
    current_scene['updated']=True
    scene.save()
    print("WHAT")
    flash('Frame generation added to queue.', 'success')
    return redirect(url_for('scene.view_scene', scene_id=scene_id))

@app.route('/generate_video/<int:scene_id>', methods=['POST'])
def generate_video_for_scene(scene_id):
    scene = Scene(data_dir)
    scene.load()
    scenes = scene.get_scenes()
    
    if scene_id < 1 or scene_id > len(scenes):
        flash('Invalid scene ID', 'error')
        return redirect(url_for('scene.view_scenes'))
    
    current_scene = scenes[scene_id - 1]
    frame_path = current_scene.get('frame', {}).get('output_path')
    
    if not frame_path or not os.path.exists(frame_path):
        flash('Frame must be generated before creating video.', 'error')
        return redirect(url_for('scene.view_scene', scene_id=scene_id))

    current_scene['updated']=True
    output_file = current_scene.get('video', {}).get('output_path')
    
    conn = connect_to_db()
    queue_id = add_to_queue(conn, 1, 'video', {
        'frame_path': frame_path,
        'output_file': output_file
    })
    conn.close()
    
    current_scene['video']['queue_id'] = queue_id
    scene.save()
    
    flash('Video generation added to queue.', 'info')
    return redirect(url_for('scene.view_scene', scene_id=scene_id))
