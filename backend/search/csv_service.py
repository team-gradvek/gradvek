from django.http import HttpResponse
from neomodel import db


def parse_and_load_csv_file(csv_data):
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
        
        #Any other format is invalid and will trigger a 400 response. User should fix file format and retry
        case _:
            return HttpResponse('Invalid format', status=400)
        
    return HttpResponse('CSV Finished loading', status=201)

def load_drug_to_ae_data_from_csv(csv_data):
    node_label = 'AssociatedWith'
    dataset = f"{'csv_upload'} {node_label}"

    # Iterate over every line in csv file
    for row in csv_data:
        # Confirm there are two entries in the line, one more chemblId and one for medraId
        if len(row) != 2:
            print(f"Invalid row: {row}. For drug to adverse event csv file load, each row must have exactly two entries, one chembl_Id and one code/meddra_Id")
            continue

        # Confirm drug exists in neo4j db Drug table by looking up the chemblId. Skip the line if it doesn't exist in the db.
        chemblId = row[0].upper()
        cypher_query = "MATCH (d:Drug {chemblId: $chemblId}) RETURN d"
        result, _ = db.cypher_query(cypher_query, {"chemblId": chemblId})
        if len(result) == 0:
            print("Skipping row. No drug found with chemblId: " + chemblId)
            continue

        # Confirm adverse event exists in neo4j db adverse event table by looking up the meddraId. Skip the line if it doesn't exist in the db.
        meddraId = row[1].upper()
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
    node_label = 'AssociatedWith'
    dataset = f"{'csv_upload'} {node_label}"

    # Iterate over every line in csv file
    for row in csv_data:
        # Confirm there are two entries in the line, one EGID and one EFO_ID
        if len(row) != 2:
            print(f"Invalid row: {row}. For target to disease csv file load, each row must have exactly two entries, one EGID and one EFO_ID")
            continue

        # Confirm target exists in neo4j db adverse event table by looking up the EGID/ensembleId. Skip the line if it doesn't exist in the db.
        ensembleId = row[0].upper()
        print(ensembleId)
        cypher_query = "MATCH (t:Target {ensembleId: $ensembleId}) RETURN t"
        result, _ = db.cypher_query(cypher_query, {"ensembleId": ensembleId})
        if len(result) == 0:
            print("Skipping row. No target found with ensembleId: " + ensembleId)
            continue

        # Confirm disease exists in neo4j db disease table by looking up the diseaseId/EFO_ID. Skip the line if it doesn't exist in the db.
        diseaseId = row[1].upper()
        print(diseaseId)
        cypher_query = "MATCH (d:Disease {diseaseId: $diseaseId}) RETURN d"
        result, _ = db.cypher_query(cypher_query, {"diseaseId": diseaseId})
        if len(result) == 0:
            print("Skipping row. No drug found with diseaseId: " + diseaseId)
            continue
        
        # Check if a relationship already exists between the target and disease so as not to overwrite it with a 0 weight.
        cypher_query = """
            MATCH (t:Target {ensembleId: $ensembleId})
            MATCH (d:Disease {diseaseId: $diseaseId})
            MATCH (t)-[r:ASSOCIATED_WITH {dataset: $dataset}]->(d)
            RETURN r
        """
        result, _ = db.cypher_query(cypher_query, {"ensembleId": ensembleId, "diseaseId": diseaseId, "dataset": dataset})

        if len(result) > 0:
            print("An ASSOCIATED_WITH relationship already exists between target " + ensembleId + " and disease " + diseaseId)
            continue

        #Create Associated_With query between target and disease
        cypher_query = """
            MATCH (t:Target {ensembleId: $ensembleId}), (d:Disease {diseaseId: $diseaseId})
            MERGE (t)-[:ASSOCIATED_WITH {dataset: $dataset, critval: 0, llr: 0}]->(d)
        """
        db.cypher_query(cypher_query, {"ensembleId": ensembleId, "diseaseId": diseaseId, "dataset": dataset})
        print("Associated_With relationship created for ensembleId: " + ensembleId + "and diseaseId " + diseaseId)