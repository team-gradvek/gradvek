# Installation

[First Pull](#first-pull)  
[How to run frontend and backend](#how-to-run-the-frontend-and-backend)  
[Makefile commands](#makefile-commands)  
[Errors](#errors)

# First Pull

## 0. Check Environment and Get Dependencies
Run the check_environment.sh script to check if you have the necessary tools and dependencies in your current environment.
```bash
./check_environment.sh
```

## 1. (OPTIONAL) Setup python environment 
Note: If you create a Python env (with a different name), add it to the .gitingore file

`cd` into `backend` folder

```
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
```

## 2. Install Python modules
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

```
pip3 install -r requirements.txt
```
## 3. Run Django Migration

`cd` into `backend` folder

```
python3 manage.py migrate
```
https://stackoverflow.com/questions/29980211/django-1-8-whats-the-difference-between-migrate-and-makemigrations

## 4. Run Admin Config


`cd` into `backend` folder  

Create a user:

```
python3 manage.py createsuperuser
```
Run the backend server:
```
python3 manage.py runserver
```
test at : http://localhost:8000/admin/  


## 5. Create descriptor objects (optional - only to showcase a database example)

Log-in to admin and add a few descriptors http://localhost:8000/admin/

## 6. Install node_modules

`cd` into `frontend` folder

Browse to the `frontend` folder and install modules
```
npm i
```
https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

# How to run the frontend and backend
## 1. Run Frontend

`cd` into frontend folder

```
npm run dev
```
http://localhost:3000/

## 2.  Run Backend

`cd` into backend folder

```
python3 manage.py runserver
```
http://localhost:8000/

## 3. To see API example
http://localhost:3000/test  
http://localhost:8000/api/descriptors

# Makefile commands

## 1. Start the Neo4j Database
```bash
make run-neo4j
```
## 2. Stop the Neo4j Database
```bash
make stop-neo4j
```

## 3. Clean the Neo4j Database

```bash
make clean
```
## 4. Get Datasets

To fetch the parquet data sets, run the `get_datasets.py` script in the `datasets` folder. This will download the data sets and save them in the `datasets/opentarget` folder. 

```bash
make get-datasets
```

## 5. Send Data to Neo4j

To parse the parquet data sets to insert into the database, run the `parse_datasets.py` script in the `datasets` folder. This will parse the data sets send the appropriate data to the database. 

This must have the Neo4j database running in order to work.

```bash
make send-data
```

# Errors

## How to resolve  SSL: CERTIFICATE_VERIFY_FAILED error 
https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
<<<<<<<<< Temporary merge branch 1

"Once upon a time I stumbled with this issue. If you're using macOS go to Macintosh HD > Applications > Python3.6 folder (or whatever version of python you're using) > double click on "Install Certificates.command" file. :D"

"If you install Python using Homebrew that file does not exist. The solution is here:"
https://stackoverflow.com/questions/44649449/brew-installation-of-python-3-6-1-ssl-certificate-verify-failed-certificate/44649450#44649450


=========
```
"Once upon a time I stumbled with this issue. If you're using macOS go to Macintosh HD > Applications > Python3.6 folder (or whatever version of python you're using) > double click on "Install Certificates.command" file. :D"
```
>>>>>>>>> Temporary merge branch 2

