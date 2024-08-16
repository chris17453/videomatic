import os
import yaml
from .flux import flux_image
from .ffmpeg import get_video_length, stretch_video, combine_videos, add_audio_to_video
import subprocess

class Scene:
    def __init__(self, base_dir,audio=None):
        self.base_dir =base_dir
        self.scene_dir =os.path.join(base_dir,"scene")
        self.frame_dir=os.path.join(base_dir,"frames")
        self.video_dir=os.path.join(base_dir,"videos")
        self.audio_dir=os.path.join(base_dir,"audio")
        if audio:
            self.audio=os.path.join(self.audio_dir,audio)
        else: 
            self.audio=None
        self.scenes = []
        self.total_length = 0
        self.templates=[]
  
        # Create directories if they don't exist
        self.create_directories()

    def create_directories(self):
        os.makedirs(self.scene_dir, exist_ok=True)
        os.makedirs(self.frame_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)        

    def add_scene(self, name, length, prompt, timestamp=None):
        if timestamp is None:
            timestamp = self.total_length
        
        scene = {
            "name": name,
            "length": length,
            "prompt": prompt,
            "timestamp": timestamp
        }
        self.scenes.append(scene)
        self.scenes.sort(key=lambda x: x["timestamp"])  # Sort scenes by timestamp
        self._update_timestamps_and_total_length()

    def _update_timestamps_and_total_length(self):
        self.total_length = 0
        current_timestamp = 0
        for i, scene in enumerate(self.scenes, start=1):
            scene["id"] = i
            scene["timestamp"] = current_timestamp
            current_timestamp += scene["length"]
            self.total_length += scene["length"]

    def get_scenes(self):
        return self.scenes

    def save(self, filename="scenes.yaml"):
        with open(os.path.join(self.scene_dir, filename), 'w') as file:
            yaml.dump({
                "scenes": self.scenes,
                "total_length": self.total_length
            }, file)

    def load(self, filename="scenes.yaml"):
        with open(os.path.join(self.scene_dir, filename), 'r') as file:
            data = yaml.safe_load(file)
            self.scenes = data.get("scenes", [])
            self.total_length = data.get("total_length", 0)
            self._update_timestamps_and_total_length()

    def create_template(self, name, template, duration=6):
        tpl = {
            'name': name,
            'template': template,
            'duration': duration
        }
        self.templates.append(tpl)

    def get_template_by_name(self, name):
        for template in self.templates:
            if template['name'] == name:
                return template
        return None

    def create_scenes_from_template(self, data, template_name, start_time=0):
        template = self.get_template_by_name(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found.")
        
        duration = template['duration']
        if start_time==0:
            start_time=self.total_length

        timestamp = start_time
        
        for item in data:
            prompt_tpl = template['template'].format(item=item)
            self.add_scene(template_name, duration, prompt_tpl, timestamp)
            timestamp += duration


    def correct_fragments(self, redo=False, indexes=None):
        for scene in self.scenes:
            input_file =  os.path.join(self.video_dir, f"vid_{scene['id']:04d}.webm")
            scene['video'] = input_file
            output_file = os.path.join(self.video_dir,'temp', f"vid_{scene['id']:04d}.mp4")
            stretch_video(input_file, output_file,scene['length'])

    def build(self):
        files=[]
        for scene in self.scenes:
            input_file =  os.path.join(self.video_dir, 'temp',f"vid_{scene['id']:04d}.mp4")
            scene['video'] = input_file
            files.append(input_file)
        output_file =  os.path.join(self.base_dir, f"videomatic.mp4")
        scene['output'] = output_file
        output_file2 =  os.path.join(self.base_dir, f"videomatic-a.mp4")
        scene['output2'] = output_file
    
        combine_videos(files,output_file)
        if self.audio:
            add_audio_to_video(output_file,self.audio,output_file2)

    
    def build_frames(self, redo=False, indexes=None):
        if not os.path.exists(self.frame_dir):
            os.makedirs(self.frame_dir)
        if redo:
            print (indexes)
        for scene in self.scenes:
            if scene['prompt']==None:
                continue
            filename = os.path.join(self.frame_dir, f"frame_{scene['id']:04d}.png")
            scene['frame'] = filename  

            if  redo:
                if  (indexes is None or scene['id'] not in indexes):
                    continue
            else:
                if os.path.exists(filename):
                    continue

            flux_image(prompt=scene['prompt'], output_file=filename)



