# Makefile

# Define compose files
DOCKER_COMPOSE_FILE := docker-compose.yml
DOCKER_COMPOSE_FILE_NEO4j := docker-compose-neo4j-local-test.yml

# Get the current user ID and group ID
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

# Export the user ID and group ID for use in docker-compose
export CURRENT_UID
export CURRENT_GID

# Default Target: Run all parts using Docker Compose
default: run-all

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

# Run all parts using Docker Compose
.PHONY: run-all
run-all: # Run all parts using Docker Compose
	$(info Make: Running all parts using Docker Compose.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

# Run Neo4j using Docker Compose
.PHONY: run-neo4j
run-neo4j: # Run Neo4j using Docker Compose
	$(info Make: Running Neo4j using Docker Compose.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE_NEO4j) up -d neo4j

# Stop all parts using Docker Compose
.PHONY: stop-all
stop-all: # Stop all parts using Docker Compose
	$(info Make: Stopping all parts using Docker Compose.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) down

# Stop Neo4j container without removing the data and logs
.PHONY: stop-neo4j
stop-neo4j: # Stop Neo4j container
	$(info Make: Stopping Neo4j container.)
	@docker-compose -f $(DOCKER_COMPOSE_FILE_NEO4j) stop neo4j

# Remove Neo4j data and logs without stopping the container
.PHONY: remove-neo4j-data-logs
remove-neo4j-data-logs: # Remove Neo4j data and logs
	$(info Make: Removing Neo4j data and logs.)
	@rm -rf ./neo4j/data/*
	@rm -rf ./neo4j/logs/*

# Remove all parts, data, and logs
.PHONY: clean
clean: # Stop and remove all parts, and clean up data and logs
	$(info Make: Stopping all parts and cleaning up data and logs.)
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

# Stop the Next.js frontend
.PHONY: stop-frontend
stop-frontend: # Stop the Next.js frontend
	$(info Make: Stopping the Next.js frontend.)
	@cd frontend && npm run stop

# Stop the Django backend
.PHONY: stop-backend
stop-backend: # Stop the Django backend
	$(info Make: Stopping the Django backend.)
	@cd backend && killall -9 python3

# Run the deployed version of the application from Docker Hub
.PHONY: run-deployed
run-deployed: # Run the deployed version of the application from Docker Hub
	$(info Make: Running all parts using Docker Compose.)
	@docker-compose -f docker-compose-published.yml up -d

# Stop the (local) deployed version of the application pulled from Docker Hub
.PHONY: stop-deployed
stop-deployed: # Stop the (local) deployed version of the application pulled rom Docker Hub
	$(info Make: Stopping all parts using Docker Compose.)
	@docker-compose -f docker-compose-published.yml stop

# Flush the Django database
.PHONY: flush-django-db
flush-django-db: # Flush the Django database
	$(info Make: Flushing Django database.)
	@cd backend && python3 manage.py flush --no-input

# Perform Django migrations
.PHONY: migrate-django-db
migrate-django-db: # Perform Django migrations
	$(info Make: Performing Django migrations.)
	@cd backend && python3 manage.py makemigrations && python3 manage.py migrate
