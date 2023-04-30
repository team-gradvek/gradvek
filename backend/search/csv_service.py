import locale
import os
import re
import string
from django.http import JsonResponse
from django.urls import URLPattern, URLResolver
from neomodel import db, config
from neomodel import NodeSet
from neomodel.core import NodeMeta
from neomodel.relationship import RelationshipMeta
from py2neo import Path
import csv

# Import local modules
#from .Cytoscape import Node, Relationship
#from .queries.actions import get_actions
#from .queries.datasets import DATASETS
#from .queries.mouse_pheno import get_pheno
#from neo4j import GraphDatabase
#import json
#from typing import List, Dict, Tuple, Union


URI = "bolt://localhost:7687"
AUTH = ("neo4j", "gradvek1")

# Dataset name
data_version = None

def set_dataset_name():
    global data_version
    with open("../datasets/platform.conf", "r") as file:
        for line in file:
            # Remove whitespace from the beginning and end of the line
            stripped_line = line.strip()

            # Check if the line starts with "data_version ="
            if stripped_line.startswith("data_version ="):
                # Split the line at the equals sign and take the second part (the value)
                data_version = stripped_line.split("=")[1].strip().replace('"', '')

    # Check if the dataset variable was set
    if data_version is None:
        raise ValueError("data_version not found in platform.conf.")
    else:
        print("Dataset version in platform.conf file:", data_version)


def parse_and_load_csv_file(csv_data):
    set_dataset_name()
    #Get header from csv file
    header = next(csv_data)

    #Concatenate header line entries so we can use switch statement 
    headerKey = ""
    for h in header:
        headerKey = headerKey + h

    match headerKey.upper():
        #For loading drug to adverse events. Chembl Id is the drug's id. Code is the adverse event meddra id
        case "CHEMBL_IDCODE":
            load_drug_to_ae_data_from_csv(csv_data)

        #For loading target to disease csv file. EGID is the ensembleId for a target and EFO_ID is the diseaseId for the disease 
        case "EGIDEFO_ID":
            load_target_to_disease_from_csv(csv_data)
            



def load_drug_to_ae_data_from_csv(csv_data):
    node_label = 'AssociatedWith'
    dataset = f"{data_version} {node_label}"

    # Iterate over every line in csv file
    for row in csv_data:
        # Confirm there are two entries in the line, one more chemblId and one for medraId
        if len(row) != 2:
            print(f"Invalid row: {row}. For drug to adverse event csv file load, each row must have exactly two entries, one chembl_Id and one code/meddra_Id")
            continue

        # Confirm drug exists in neo4j db Drug table by looking up the chemblId. Skip the line if it doesn't exist in the db.
        chemblId = row[0].upper()
        print(chemblId)
        cypher_query = "MATCH (d:Drug {chemblId: $chemblId}) RETURN d"
        result, _ = db.cypher_query(cypher_query, {"chemblId": chemblId})
        if len(result) == 0:
            print("Skipping row. No drug found with chemblId: " + chemblId)
            continue

        # Confirm adverse event exists in neo4j db adverse event table by looking up the meddraId. Skip the line if it doesn't exist in the db.
        meddraId = row[1].upper()
        print(meddraId)
        cypher_query = "MATCH (d:AdverseEvent {meddraId: $meddraId}) RETURN d"
        result, _ = db.cypher_query(cypher_query, {"meddraId": meddraId})
        if len(result) == 0:
            print("Skipping row. No adverse event found with meddraId: " + meddraId)
            continue
        
        # Check if a relationship already exists between the drug and adverse event so as not to overwrite it with a 0 weight.
        cypher_query = """
            MATCH (d:Drug {chemblId: $chemblId})
            MATCH (a:AdverseEvent {meddraId: $meddraId})
            MATCH (d)-[r:ASSOCIATED_WITH {dataset: $dataset}]->(a)
            RETURN r
        """
        result, _ = db.cypher_query(cypher_query, {"chemblId": chemblId, "meddraId": meddraId, "dataset": dataset})

        if len(result) > 0:
            print("An ASSOCIATED_WITH relationship already exists between drug " + chemblId + " and adverse event " + meddraId)
            continue
        
        #Create Associated_With query between drug and adverse event
        cypher_query = """
            MATCH (d:Drug {chemblId: $chemblId}), (ae:AdverseEvent {meddraId: $meddraId})
            MERGE (d)-[:ASSOCIATED_WITH {dataset: $dataset, critval: 0, llr: 0}]->(ae)
        """
        db.cypher_query(cypher_query, {"chemblId": chemblId, "meddraId": meddraId, "dataset": dataset})
        print("Associated_With relationship created for chemblId: " + chemblId + "and meddraId " + meddraId)






def load_target_to_disease_from_csv(csv_data):
    pass