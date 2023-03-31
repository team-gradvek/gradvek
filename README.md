# Installation

[First Pull](https://github.com/team-gradvek/gradvek#first-pull)  
[How to run frontend and backend](https://github.com/team-gradvek/gradvek#how-to-run-the-frontend-and-backend)  
[Make file commands](https://github.com/team-gradvek/gradvek#make-file-commands)  

# First Pull

### 1. Setup python environment (optional)
Note: If you create a Python env (with a different name), add it to the .gitingore file

`cd` into `backend` folder

```
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
```


### 2. Install Python modules
Note: if you created a Python env, install the modules inside the environement. 
To start the env:

```
source env/bin/activate 
```
To stop the env:
```
deactivate 
```


`cd` into `backend` folder

```
pip3 install -r requirements.txt
```

### 3. Run Django Migration

`cd` into `backend` folder

```
python3 manage.py migrate
```
https://stackoverflow.com/questions/29980211/django-1-8-whats-the-difference-between-migrate-and-makemigrations

### 4. Run Admin Config

`cd` into `backend` folder

```
python3 manage.py createsuperuser
```
test at : http://localhost:8000/admin/

### 5. Create descriptor objects (optional - only to showcase a database example)

Log-in to admin and add a few descriptors http://localhost:8000/admin/


### 6. Install node_modules

`cd` into `frontend` folder

Browse to the `frontend` folder and install modules
```
npm i
```
https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

# How to run the frontend and backend
### 1. Run Frontend

`cd` into frontend folder

```
npm run dev
```
http://localhost:3000/

### 2.  Run Backend

`cd` into backend folder

```
python3 manage.py runserver
```
http://localhost:8000/

# Make file commands


