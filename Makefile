

# builds a single video from video fragments and adds audio track
build: frames videos reformat
	@python -m videomatic.cli build

# creates image frames used for video creation
frames:
	@python -m videomatic.cli create_frames

# creates video fragments
videos:
	@python -m videomatic.cli create_videos

# Stretches and interploats fragments
reformat:
	@python -m videomatic.cli reformat_video