

build:
	@python -m videomatic.cli build

send_frames:
	scp  data/frames/*.png gpu2.watkinslabs.com:/home/nd/frames/
	ssh -t gpu2.watkinslabs.com "bash -c 'sudo rm -rf /home/ai-services/apps/comfyui/input/* && sudo mv /home/nd/frames/*.png   /home/ai-services/apps/comfyui/input/ && sudo chown ai-services:www-data /home/ai-services/apps/comfyui/input/'"

get_vids:
	ssh -t gpu2.watkinslabs.com "sudo cp -r /home/ai-services/apps/comfyui/output/ /home/nd/ && sudo chown nd:nd /home/nd/output"
	scp   gpu2.watkinslabs.com:/home/nd/output/*.webm data/videos/

# not used
stitch:
	ffmpeg -f concat -safe 0 -i data/videos/stitch.txt -c copy data/combined.mp4

