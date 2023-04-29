# Makefile

# Variables
# Set the Docker Compose file for running Neo4j
DOCKER_COMPOSE_FILE := docker-compose-neo4j-local-test.yml

# Get the current user ID and group ID
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

# Export the user ID and group ID for use in docker-compose
export CURRENT_UID
export CURRENT_GID

# Default Target: Run Neo4j using Docker Compose
default: run-neo4j

# Display help for each command in the Makefile
.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Check the environment for the correct tools and dependencies
.PHONY: check-environment
check-environment: # Run the check_environment.sh script to verify the environment
	$(info Make: Checking the environment for the correct tools and dependencies.)
	@./check_environment.sh

# Download datasets using the get_datasets.py script
.PHONY: get-datasets
get-datasets: # Get datasets using the get_datasets.py script
	$(info Make: Getting datasets.)
	@cd backend/datasets && python3 get_datasets.py

# Import data into Neo4j using the parse_datasets.py script
.PHONY: send-data
send-data: # Send data to Neo4j using the parse_datasets.py script
	$(info Make: Sending data to Neo4j.)
	@cd backend/datasets && python3 parse_datasets.py

# Run the Neo4j container using Docker Compose
.PHONY: run-neo4j
run-neo4j: # Run Neo4j using Docker Compose
	$(info Make: Running Neo4j using Docker Compose.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

# Stop the Neo4j container without removing the data and logs
.PHONY: stop-neo4j
stop-neo4j: # Stop the Neo4j container
	$(info Make: Stopping Neo4j container.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) stop

# Remove Neo4j data and logs without stopping the container
.PHONY: remove-data-logs
remove-data-logs: # Remove Neo4j data and logs
	$(info Make: Removing Neo4j data and logs.)
	@rm -rf ./neo4j/data/*
	@rm -rf ./neo4j/logs/*

# Remove the Neo4j container, data, and logs
.PHONY: clean
clean: # Stop and remove the Neo4j container and clean up data and logs
	$(info Make: Stopping Neo4j container and cleaning up data and logs.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) down
	@rm -rf ./neo4j/data/*
	@rm -rf ./neo4j/logs/*

# Run the Next.js frontend
.PHONY: run-frontend
run-frontend: # Run the Next.js frontend
	$(info Make: Running the Next.js frontend.)
	@cd frontend && npm run dev

# Run the Django backend
.PHONY: run-backend
run-backend: # Run the Django backend
	$(info Make: Running the Django backend.)
	@cd backend && python3 manage.py runserver

