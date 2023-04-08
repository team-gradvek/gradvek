# Makefile

# Variables
DOCKER_COMPOSE_FILE := docker-compose-neo4j-local-test.yml

CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

export CURRENT_UID
export CURRENT_GID

# Default Target
.PHONY: run-neo4j
default: run-neo4j

# Get datasets using the get_datasets.py script
get-datasets:
	$(info Make: Getting datasets.)
	@cd datasets && python3 get_datasets.py

# Send data using the parse_datasets.py script
send-data:
	$(info Make: Sending data to Neo4j.)
	@cd datasets && python3 parse_datasets.py

# Run Neo4j with docker-compose
run-neo4j:
	$(info Make: Running Neo4j using Docker Compose.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

# Stop Neo4j container without removing data and logs
.PHONY: stop-neo4j
stop-neo4j:
	$(info Make: Stopping Neo4j container.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) stop

# Remove Neo4j data and logs without stopping the container
.PHONY: remove-data-logs
remove-data-logs:
	$(info Make: Removing Neo4j data and logs.)
	@rm -rf ./neo4j/data/*
	@rm -rf ./neo4j/logs/*

# Clean command for stopping the Neo4j container and removing data and logs
.PHONY: clean
clean:
	$(info Make: Stopping Neo4j container and cleaning up data and logs.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) down
	@rm -rf ./neo4j/data/*
	@rm -rf ./neo4j/logs/*
