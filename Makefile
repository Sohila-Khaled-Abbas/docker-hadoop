.PHONY: help build up down restart logs ps test bash hdfs-shell clean

help:
	@echo "Available commands:"
	@echo "  make build       - Build the Hadoop Docker image"
	@echo "  make up          - Start the Hadoop single-node cluster"
	@echo "  make down        - Stop and remove the Hadoop cluster"
	@echo "  make restart     - Restart the Hadoop cluster"
	@echo "  make logs        - Tail container logs"
	@echo "  make ps          - List running services and status"
	@echo "  make test        - Run MapReduce and HDFS integration tests"
	@echo "  make bash        - Open an interactive bash terminal inside the container"
	@echo "  make hdfs-shell  - Open HDFS CLI as hduser"
	@echo "  make clean       - Remove containers, images, and volumes"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

ps:
	docker compose ps

test:
	docker compose exec hadoop /test-cluster.sh

bash:
	docker compose exec hadoop bash

hdfs-shell:
	docker compose exec -u hduser hadoop bash

clean:
	docker compose down -v --rmi all
