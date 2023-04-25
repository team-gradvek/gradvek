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
### 2. Check your environment
Run the check_environment.sh script to verify that your environment has the necessary tools and dependencies:
```Bash
./check_environment.sh
```

## 3. Add .env file inside Django project

```makefile
SECRET_KEY=
NEO4J_USERNAME=
NEO4J_PASSWORD=
NEO4J_BOLT_URL=
```
The secret keys can be found in the team's private repository at https://github.com/team-gradvek/env.

### 4. Setup the Django backend
#### 4.1. (Optional) If you want to use a virtual environment for Python, first navigate to the backend folder and follow these steps:

```Bash
cd backend
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
```
#### 4.2. Install Python dependencies:
Note: if you created a Python env in step 1, install the modules inside the environement. 
To start the env:

```
source env/bin/activate 
```

To stop the env:

```
deactivate 
```

Update to Python 3.11  

```
https://www.python.org/downloads/
```

Get Django  

MacOS/Linux:

```
 brew install django-completion
```
Windows:

```
https://docs.djangoproject.com/en/4.1/howto/windows/
```
Update to Python 3.11  

```
https://www.python.org/downloads/
```

Get Django  

MacOS/Linux:

```
 brew install django-completion
```
Windows:

```
https://docs.djangoproject.com/en/4.1/howto/windows/
```

`cd` into `backend` folder

```Bash
pip3 install -r requirements.txt
```
#### 4.3. Run Django migrations:
```Bash
python3 manage.py migrate
```
https://stackoverflow.com/questions/29980211/django-1-8-whats-the-difference-between-migrate-and-makemigrations

## 5. (OPTIONAL) Run Admin Config


`cd` into `backend` folder  

Create a user:

```
python3 manage.py createsuperuser
```


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
```bash
cd backend
python3 manage.py runserver
```
Visit http://localhost:8000/ to ensure the backend is running.
Note: The Neo4j database must be running for the backend to work.

## Makefile commands
### 1. Start the Neo4j database
```bash
make run-neo4j
```
### 2. Stop the Neo4j database
```bash
make stop-neo4j
```
### 3. Clean the Neo4j database
```bash
make clean
```
### 4. Get datasets
To fetch the Parquet datasets, run the get_datasets.py script in the datasets folder:

```bash
make get-datasets
```
### 5. Send data to Neo4j
To parse the Parquet datasets and insert them into the database, run the parse_datasets.py script in the datasets folder:

```bash
make send-data
```
Note: The Neo4j database must be running for this command to work.

# Errors

## How to resolve  SSL: CERTIFICATE_VERIFY_FAILED error 
https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org

"Once upon a time I stumbled with this issue. If you're using macOS go to Macintosh HD > Applications > Python3.6 folder (or whatever version of python you're using) > double click on "Install Certificates.command" file."

## Neo4j/Docker Connection Errors
https://stackoverflow.com/questions/42397751/neo4j-in-docker-max-heap-size-causes-hard-crash-137/42398497#42398497

