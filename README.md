# Installation 

## Pull repo

```
git pull 
```

## Setup python environment (optional)

`cd` into backend folder

```
python3 -m venv env
source env/bin/activate
```

## Install python modules

`cd` into backend folder

```
pip install -r requirements.txt
```

## Run Migration

`cd` into backend folder

```
python3 manage.py migrate
```

# Run Admin Config

`cd` into backend folder

```
python3 manage.py createsuperuser
```

## Create Descriptor

Log-in to admin and add a new descriptor


## Install node_modules

`cd` into frontend folder

Browse to the frontend folder and install modules
```
npm i
```

## Run Frontend

`cd` into frontend folder

```
npm run dev
```

## Run Backend

`cd` into backend folder

```
python3 manage.py runserver
```




