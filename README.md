# GradVek
GradVek (GRaph of ADVerse Event Knowledge) is a project aimed at providing an interface for searching drug target information and finding adverse events for similar targets. It includes a Django backend, a Neo4j database, and a Next.js frontend.

### Table of Contents
* [Setup](#Setup)  
* [Running the project](#running-the-project)  
* [Makefile commands](#makefile-commands)  
* [Errors](#errors)  

## Setup
Follow these steps to set up the GradVek project:

### 1. Clone the repository
```Bash
git clone https://github.com/team-gradvek/gradvek
cd gradvek
```

### 2. (OPTIONAL) If you want to use a virtual environment for Python, first navigate to the backend folder and follow these steps:

```Bash
cd backend
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
```
Note: if you created a Python env install the modules inside the environment.   
To start the env:

```
source env/bin/activate 
```

To stop the env:

```
deactivate 
```
### 3. Check your environment
Note: if you created a Python env install the modules inside the environment.   
Run the check_environment.sh script to verify that your environment has the necessary tools and dependencies:
```Bash
./check_environment.sh
```
Windows: you may need to change `python3` for `python`  

### 4. Add `.env` file inside Django project

`cd backend/gradvekbackend `

```
SECRET_KEY=
NEO4J_USERNAME=
NEO4J_PASSWORD=
NEO4J_BOLT_URL=
```
The secret keys can be found in the team's private repository at https://github.com/team-gradvek/env.


## Running the project
### 1. Install Node.js modules and Run the Next.js frontend

Navigate to the frontend folder and install the required Node.js modules:
```Bash
cd frontend
npm i
```
https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

```bash
cd frontend
npm run dev
```
Open your browser and navigate to http://localhost:3000/.

### 2. Run the Django backend

#### 2.1 Run Django migrations:
Note: For the names of the nine descriptors used in this project, we constructed a basic Django model. This can be changed in the future.

```Bash
python3 manage.py migrate
```
https://stackoverflow.com/questions/29980211/django-1-8-whats-the-difference-between-migrate-and-makemigrations

#### 2.2 Run Admin Config
`cd` into `backend` folder  

Create a user:

```
python3 manage.py createsuperuser
```
#### 2.3 Run Django backend
```bash
cd backend
python3 manage.py runserver
```
Visit http://localhost:8000/ to ensure the backend is running.
Note: The Neo4j database must be running for the backend to work.


## Makefile commands

| Command                       | Description                                                  |
|-------------------------------|--------------------------------------------------------------|
| `make` or `make run-all`      | Run the complete application in Docker                       |
| `make help`                   | Show help for each of the Makefile recipes                   |
| `make check-environment`      | Check the environment for the correct tools and dependencies |
| `make get-datasets`           | Fetch the Parquet datasets                                   |
| `make send-data`              | Parse the Parquet datasets and insert them into the database |
| `make run-neo4j`              | Start the Neo4j database                                     |
| `make stop-all`               | Stop all parts using Docker Compose                          |
| `make stop-neo4j`             | Stop the Neo4j database                                      |
| `make remove-neo4j-data-logs` | Remove Neo4j data and logs                                   |
| `make clean`                  | Stop and remove all parts, and clean up data and logs        |
| `make run-frontend`           | Run the Next.js frontend                                     |
| `make run-backend`            | Run the Django backend                                       |
| `make stop-frontend`          | Stop the Next.js frontend                                    |
| `make stop-backend`           | Stop the Django backend                                      |
| `make run-deployed`           | Start the version of the application published to Docker hub |
| `make stop-deployed`          | Stop the version of the application published to Docker hub  |

_Note: The Neo4j database must be running for the `make send-data` or the `make run-backend` command to work._
_Note: SECRET_KEY must be set in docker-compose-published.yml for `make run-deployed` command to work._


# Errors

## How to resolve  SSL: CERTIFICATE_VERIFY_FAILED error 
https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org

"Once upon a time I stumbled with this issue. If you're using macOS go to Macintosh HD > Applications > Python3.6 folder (or whatever version of python you're using) > double click on "Install Certificates.command" file."

## Neo4j/Docker Connection Errors
https://stackoverflow.com/questions/42397751/neo4j-in-docker-max-heap-size-causes-hard-crash-137/42398497#42398497

