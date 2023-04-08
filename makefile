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

# Run Neo4j with docker-compose
run-neo4j:
	$(info Make: Running Neo4j using Docker Compose.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

# Cleanup command for deleting Neo4j data and logs
.PHONY: clean
clean:
	$(info Make: Cleaning up Neo4j image, data and logs.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) down
	@rm -rf ./neo4j/data/*
	@rm -rf ./neo4j/logs/*
