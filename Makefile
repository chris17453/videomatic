
DOCKER = docker
DOCKER_COMPOSE = docker compose
DB_IMAGE_NAME = videomatic-db
DB_CONTAINER_NAME = videomatic-db-container
VIDEOMATIC_DB_YAML = postgres-dockerfile

.PHONY: frames videos reformat web

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

web:
	@python -m web.app

queue:
	@python -m videomatic.queue

flort:
	@flort --py --sql videomatic web containers

# Build the Docker image
container-build:
	@cd containers && $(DOCKER_COMPOSE) build

# Start the container
up:
	@cd containers && $(DOCKER_COMPOSE)  up -d

# Stop the container
down:
	@cd containers && $(DOCKER_COMPOSE) down

# Stop the container
del:
	@cd containers && $(DOCKER_COMPOSE) down -v

# Restart the container
restart: down up

logs:
	@docker logs containers-db-1  -f

init:
	@docker cp ./containers/init.sql containers-db-1:/tmp/init.sql
	@docker exec -i containers-db-1 psql -U vidma-sa -d videomatic -f /tmp/init.sql

