# GradVek
GradVek (GRaph of ADVerse Event Knowledge) is a project aimed at providing an interface for searching drug target information and finding adverse events for similar targets. It includes a Django backend, a Neo4j database, and a Next.js frontend.

### Table of Contents

* [Setup](#Setup)  
* [Running the project](#running-the-project)  
* [Makefile commands](#makefile-commands)  
* [Errors](#errors)  
* [Design of System](#design-of-system)
* [Screenshots](#screenshots)  




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
Windows: you may need to change `python3` for `python` inside check_environement.sh


```Bash
cd backend
pip3 install -r requirements.txt 
```

Project requires Python 3.11 or above  


### 4. Add `.env` file inside Django project

`cd backend/gradvekbackend `

```
SECRET_KEY=django-insecure-hr#d_z6nfthw)r=0f96mhgfg6pk34-ob%ez+--ci4l$)tro*&b
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=gradvek1
NEO4J_BOLT_URL=bolt://neo4j:gradvek1@localhost:7687
```

## Running the application
You can run the app locally or with Docker. Check the makefile commands:
[Makefile commands](#makefile-commands)   

**The steps below describe how to operate the frontend and backend without Docker:**

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
**Make sure Docker is running.**  
The Neo4j database must be running for the backend to work (check Makefile commands). 
```bash
cd gradvek
make run-neo4j
```
_Note: Look at the Docker logs and wait until you see "started"._

There is a startup function in Django that retrieves the Open Targets datasets and parse it to the Neo4j database. The Neo4j database must be running for the backend to work (check Makefile commands).

```bash
cd backend
python3 manage.py runserver
```
Visit http://localhost:8000/ to ensure the backend is running.

You can see the Neo4j db at http://localhost:7474/.


## Makefile commands

_Note: If `make run-all` you run the complete application in Docker it is possible the Neo4j container exits as it is competing for memory. Try restarting the Neo4j container a few times._

If you run any component of the application in Docker, please check the Docker logs to see how things are progressing.

_Note: The Neo4j database must be running for the `make send-data` or the `make run-backend` command to work._  
_Note: SECRET_KEY must be set in docker-compose-published.yml for `make run-deployed` command to work._

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



# Errors

### How to resolve  SSL: CERTIFICATE_VERIFY_FAILED error 
https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org

"If you're using macOS go to Macintosh HD > Applications > Python3.6 folder (or whatever version of python you're using) > double click on "Install Certificates.command" file."

### Neo4j/Docker Connection Errors
https://stackoverflow.com/questions/42397751/neo4j-in-docker-max-heap-size-causes-hard-crash-137/42398497#42398497

### Couldn't validate latest open targets version and update data.[Errno 2] No such file or directory: 'XXX/gradvek/datasets/opentarget/diseases’
Please manually create the folder


### Neo4j container
_Note: If `make run-all` you run the complete application in Docker it is possible the Neo4j container exits as it is competing for memory. Try restarting the Neo4j container a few times._


# Design of system
![plot](./screenshots/gradvek_diagram.png)

GradVek (GRaph of ADVerse Event Knowledge) is a software system designed to manage OpenTargets Drug data. It provides an interactive interface for users to explore and understand drug-related adverse events. This section outlines the design of the system, including frontend, backend, and database components, as well as the choice of language/platform.

### System Overview
GradVek consists of the following components:
1.	Frontend: A Next.js application offering an interactive user interface for accessing and visualizing the data. The frontend is organized into various pages and components that are built using React and use hooks for data fetching. It communicates with the backend via API endpoints, which provide the necessary data for rendering and visualization.
2.	Backend: A Django REST API retrieves data from OpenTargets, stores it in a Neo4j Graph Database, and serves various data endpoints to the frontend. The backend is organized into different sections for each of its main functions, which work together to handle data ingestion, querying, and endpoint management. It supports routes that provide all the information for the frontend to use.
3.	Data Storage: Neo4j Graph Database stores the data and enables querying and retrieval of relationships between entities. The database schema consists of nodes and relationships that represent drugs, targets, adverse events, and other relevant entities. Two Neo4j plugins are used APOC (Awesome Procedures on Cypher) and GDS (Graph Data Science) to extend its capabilities for more efficient queries and computational support.

These components interact with each other to provide a seamless user experience, allowing users to explore and understand drug-related adverse events. The system's design ensures that it can be easily maintained, expanded, and adapted to meet the evolving needs of its users.

### Frontend Design
The frontend is built using Next.js, a React-based framework offering server-side rendering, client-side rendering, caching, built-in optimizations for assets, advanced data fetching, and scalability. The frontend is designed to consume the backend API endpoints and render data in a clean interface.

The frontend is organized into a modular structure, with pages, components, hooks, and utilities. The components are built using React, and hooks are used for data fetching and managing the state. The frontend leverages libraries, such as Vis.js for graph visualization.

Frontend Pages include:
* Home: Provides an overview of the application and search options for various entities, such as drugs, targets, adverse events, and diseases, and access to other sections of the application.
* Target To Adverse Events: Displays adverse event search results and information about adverse events related to specific targets.
* Adverse Event To Target: Displays search results for targets related to a specific adverse event, allowing users to explore and understand the relationships.
* Target To Target: Displays search results for similar targets and their relationships, facilitating the discovery of commonalities between targets.
* Drug Search by Target and Adverse Event: Enables users to find drugs that have a particular target and adverse event associated, providing valuable insights into drug-target interactions and potential side effects.
* Settings: Allows users to configure the application settings, manage data sources, and view system information.
These pages are designed to be responsive, ensuring a seamless web browser experience for laptop, desktop, and several tablet mobile devices. The frontend employs a consistent color scheme and design elements throughout the application, providing a unified look and feel.

### Backend Design
The backend is built using Django, a Python web framework, along with the Django REST framework for creating an API that serves as the intermediary between the frontend and the Neo4j Graph Database. The backend is organized into three sections, the main section, search, is organized in a modular structure, with apps, models, views, serializers, and supporting utility functions working together to handle data ingestion, querying, and endpoint management. It leverages various libraries, such as neomodel for working with the Neo4j database and pandas for data processing.

The backend is divided into three sections:

* Datasets: This section contains the get_datasets.py file, which handles retrieving OpenTargets data from the FTP server, and the parse_datasets.py file, which processes the OpenTargets Parquet files and constructs APOC Cypher queries to upload the data to Neo4j with batched and parallelized processing when possible.
* Gradvekbackend: This section contains the Django app's settings and startup functions.
* Search: This section includes the URL configurations, views, utility functions, queries, and computing and retrieving similarity scores using GDS. It provides all the endpoints that the frontend uses.

On startup, the backend evaluates the Parquet data, data in Neo4j, and cached similarity score data. It runs the appropriate functions to ensure that all data is correct, available, and up-to-date automatically. The backend does not use py2neo; instead, it employs the neomodel library for working with Neo4j.

The API is responsible for the following tasks:
* Data Ingestion: The OpenTargets data is downloaded, stored, and processed as part of the startup. The backend also provides an endpoint for ingesting additional user data in the form of CSV files. Data ingestion includes processing raw data, cleaning, and transforming it into a suitable format for storage in the database.
* Querying: Fetching data from the Neo4j Graph Database based on frontend requests and transforming it into a suitable format for consumption by the frontend. It involves executing Cypher queries, aggregating results, and applying various filters and sorting options as needed. The backend also leverages Neo4j plugins like APOC and GDS to optimize query performance and conduct complex graph analysis.
* Endpoint Management: Defining various endpoints for the frontend to access, such as retrieving graph data such as paths between various entity types, searching for entities, and fetching computed data such as similarity metrics. The backend provides comprehensive API documentation using tools like Swagger, which enables developers to understand and interact with the API more effectively.


### Datasets Package Diagram
Datasets: Written entirely as functions, the two main components operate in a similar fashion

* `get_dataests.py`: Composes of several functions to manage the fetching and organization of open targets data. The download mechanism retrieves multiple files in parallel and supports a retry mechanism and graceful error handling. It is centered around a dictionary written in such a way that changing or adding more datasets is simply a matter of making a new entry, stating the name of the data type, and the source directory for the data to be retrieved.
* `parse_datasets.py`: Similar to get_dataets, this handles the parsing and is written in a way that to add data you simply need to add a line the the main dictionary with the name of the data type, and the functions that generate the desired cypher queries using that data.


### `gradvekbackend` Package Diagram
Gradvek backend is primarily django configuration, settings, and startup triggers.
![plot](./screenshots/django_config.png)

This section handles django setup and configuration, as well as startup functions triggering the functions in the datasets package, as well as handling establishing the connection between the backend and neo4j, using a retry and timeout mechanism, as well as handling connections changes between environments such as running natively or in a docker container.

### `search` Package
The search section of the backend is where the routes are provided and the backend communicates with neo4j to retrieve and compute the return results.
* `urls`: Where all the routes the backend provides are defined
* `views`: Called by Urls, takes path arguments, and passes them to util functions, organized into classes with GET and POST functions when appropriate
* `utils`: Constructs cypher queries, communicates with neo4j, and returns the results to the view, as well as additional functions to support processing retrieved data when needed.
* `cytoscape`: Provides the necessary classes to process and organize paths of data retrieved from neo4j
* Cytoscape Entity Class Diagram: Used as part of processing Target to Adverse event and Adverse Event to Target paths

![plot](./screenshots/cytoscape.png)

### Language and Platform
GradVek's choice of language and platform is influenced by the following factors:

1.	Scalability: Both Next.js and Django are known for their scalability, handling a growing user base and increasing data volumes efficiently.
2.	Ecosystem: The JavaScript and Python ecosystems have many libraries and tools that can be used to build GradVek more efficiently.
3.	Developer Experience: Next.js and Django offer a modern developer experience, built on popular languages and supporting useful features such as hot module replacement.
4.	Data Handling: Django's support for various databases and its ability to work with Neo4j make it an ideal choice for a data-intensive application like GradVek. The Neo4j Graph Database provides efficient querying and management of complex relationships between drug data entities.


# Screenshots

### http://www.gradvek.org
![plot](./screenshots/home.png)

### Target to Adverse Event
![plot](./screenshots/search1.png)
![plot](./screenshots/result1.png)

### Adverse Event to Target
![plot](./screenshots/result2.png)

### Target to Target Similarity
TARGETS BASED ON SIMILARITY: MOUSE PHENOTYPE FOR FGG
![plot](./screenshots/FGG-mouse.png)
TARGETS BASED ON SIMILARITY: AVERAGE FOR FGG
![plot](./screenshots/FGG-average.png)


### Drug Search by Target and AE
![plot](./screenshots/target-ae.png)
![plot](./screenshots/result3.png)


### Proprietary Data
![plot](./screenshots/csv.png)