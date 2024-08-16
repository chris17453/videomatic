import os
import subprocess

def get_video_length(input_file):
    """Get the duration of the video in seconds using ffmpeg."""
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(result)
    return float(result.stdout.strip())


def stretch_video(input_file, output_file, dest_length):
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get the original length of the video
    original_length = get_video_length(input_file)
    
    # Calculate the ratio of destination length to original length
    stretch_factor = original_length/dest_length 
    print(1/stretch_factor,original_length,dest_length)
    # Use ffmpeg to stretch the video
    subprocess.run([
        'ffmpeg', '-y' ,'-i', input_file,
        '-filter:v', f'setpts={1/stretch_factor}*PTS',
        '-an', output_file
    ], check=True)

   

def combine_videos(file_list, output_file):
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a temporary text file to list all the input files for ffmpeg
    list_file = 'temp_file_list.txt'
    with open(list_file, 'w') as f:
        for filename in file_list:
            f.write(f"file '{filename}'\n")

    # Use ffmpeg to concatenate the videos
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_file,
        '-c', 'copy', output_file
    ], check=True)

    # Remove the temporary list file
    os.remove(list_file)
       
def add_audio_to_video(video_file, audio_file, output_file):
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Use ffmpeg to combine the video with the audio
    subprocess.run([
        'ffmpeg', '-y', '-i', video_file, '-i', audio_file,
        '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', '-shortest',
        output_file
    ], check=True)
