from collections import defaultdict
import json
from django.shortcuts import render
from django.urls import get_resolver
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from neomodel import db


from .models import (
    Descriptor,
    # Action, 
    MousePheno,
    Hgene,
    Hprotein,
    Intact,
    NodeSimilarity,
    Pathway,
    Reactome,
    Signor,
    Gwas,
    )

from .serializers import (
    AverageNodeSimilaritySerializer,
    AverageSimilaritySerializer,
    DescriptorSerializer, 
    MousePhenoSerializer,
    HgeneSerializer,
    HproteinSerializer,
    IntactSerializer,
    NodeSimilaritySerializer,
    PathwaySerializer,
    ReactomeSerializer,
    SignorSerializer,
    GwasSerializer,
    )


from .utils import (
    count_all_entities,
    fetch_actions,
    fetch_datasets,
    # fetch_similarity,
    get_all_routes,
    get_cytoscape_entities_as_json,
    get_entity_count,
    get_paths_ae_target_drug,
    get_paths_target_ae_drug,
    get_weights_by_ae,
    get_weights_by_target,
    update_dataset_status,
    clear_neo4j_database,
    suggestion_by_hint_for_target,
    suggestion_by_hint_for_adverse_event,
    suggestion_by_hint_for_disease,
    suggestion_by_hint_for_drug,
    suggestion_by_hint_for_mouse_phenotype,
    suggestion_by_hint_for_pathway,

)


class RoutesListAPIView(generics.GenericAPIView):
    """
    API view to list all routes in the Django site
    """
    # Override the get_queryset method to return None, as we don't deal with a queryset
    def get_queryset(self):
        return None
    # Override the GET method to return the list of routes
    def get(self, request, *args, **kwargs):
        resolver = get_resolver(None)  # Get the project's URL resolver
        # Extract all routes from the URL patterns
        routes = get_all_routes(resolver.url_patterns)
        return Response(routes)  # Return the list of routes as a JSON response


class DescriptorListView(generics.ListAPIView):
    """
    Collect Descriptors list from Django db and format it
    """
    queryset = Descriptor.objects.all()
    serializer_class = DescriptorSerializer


class GetActions(APIView):
    """
    Return an array of all actions or specific to a target
    """
    def get(self, request,  *args, **kwargs):

        # Check if a target is in the requested path
        try: 
            target = self.kwargs["target"]
        # Else save as empty string
        except:
            target = ""
        # Get cypher query results
        actions = fetch_actions(target)
    
        # Return the result as a JSON response
        return Response(actions, status=status.HTTP_200_OK)


descriptor_classes = {
    "mousepheno" : [MousePheno, MousePhenoSerializer],
    "hgene": [Hgene, HgeneSerializer],
    "hprotein": [Hprotein, HproteinSerializer],
    "intact": [Intact, IntactSerializer],
    "pathway": [Pathway, PathwaySerializer],
    "reactome": [Reactome, ReactomeSerializer],
    "signor": [Signor, SignorSerializer],
    "gwas": [Gwas, GwasSerializer],
}

class GetSimilarity(APIView):

    """
    List all node similarity scores associated with a target
    """
    def get(self, request,  *args, **kwargs):
        descriptors = {
            "mousepheno": ["MousePhenotype", "MOUSE_PHENOTYPE", MousePheno, "SIMILAR_MOUSEPHENO"],
            "hgene": ["Baseline_Expression", "HGENE", Hgene, "SIMILAR_HGENE"],
            "hprotein": ["Baseline_Expression", "HPROTEIN", Hprotein, "SIMILAR_HPROTEIN"],
            "intact": ["Target", "INTACT", Intact, "SIMILAR_INTACT"],
            "pathway": ["TargetPathway", "PATHWAY", Pathway, "SIMILAR_PATHWAY"],
            "reactome": ["Target", "REACTOME", Reactome, "SIMILAR_REACTOME"],
            "signor": ["Target", "SIGNOR", Signor, "SIMILAR_SIGNOR"],
            # "gwas": ["Gwas","GWAS_RELATION", Gwas, "SIMILAR_GWAS"],
        }
        # Check if a target and descriptor is in the requested path
        try: 
            target = self.kwargs['target']
            descriptor_type = self.kwargs['descriptor']
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        type_name = descriptors.get(descriptor_type)[0]
        edge_name = descriptors.get(descriptor_type)[1]
        relationship_type = descriptors.get(descriptor_type)[3]

        # Get similarity results from Neo4j using Cypher query
        results = db.cypher_query(
            f'''
            MATCH (n1:Target {{symbol: "{target}"}})-[r:{relationship_type}]-(n2:Target)
            WHERE n1 <> n2
            RETURN n1.symbol, n2.symbol, r.score
            ORDER BY r.score DESC
            '''
        )[0]

        response_data = []
        for row in results:
            entry = {'target1': row[0], 'target2': row[1], 'similarity': row[2]}
            if entry not in response_data:
                response_data.append(entry)

        return Response(response_data)



class GetAverageSimilarity(APIView):
    """
    List the average node similarity scores for a target across all descriptors
    """

    def get(self, request, *args, **kwargs):
        descriptors = {
            "mousepheno": "SIMILAR_MOUSEPHENO",
            "hgene": "SIMILAR_HGENE",
            "hprotein": "SIMILAR_HPROTEIN",
            "intact": "SIMILAR_INTACT",
            "pathway": "SIMILAR_PATHWAY",
            "reactome": "SIMILAR_REACTOME",
            "signor": "SIMILAR_SIGNOR",
            # "gwas": "SIMILAR_GWAS",
        }

        # Check if a target is in the requested path
        try:
            target = self.kwargs['target']
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Initialize defaultdict for storing results
        descriptor_results = defaultdict(lambda: {"total": 0, "count": 0, "descriptors": set()})

        for descriptor_type, relationship_type in descriptors.items():
            # Get similarity results from Neo4j using Cypher query
            results = db.cypher_query(
                f'''
                MATCH (n1:Target {{symbol: "{target}"}})-[r:{relationship_type}]-(n2:Target)
                WHERE n1 <> n2
                RETURN n1.symbol, n2.symbol, r.score
                '''
            )[0]

            # Calculate the sum, count, and descriptors for each target2
            for row in results:
                target1, target2, similarity = row
                descriptor_results[target2]["total"] += similarity
                descriptor_results[target2]["count"] += 1
                descriptor_results[target2]["descriptors"].add(descriptor_type)

        # Calculate the averages and sort results by average in descending order
        average_scores = [
            {
                "target1": target,
                "target2": target2,
                "average": total / count,
                "descriptors": list(descriptors)
            }
            for target2, result in descriptor_results.items()
            if (total := result["total"]) and (count := result["count"]) and (descriptors := result["descriptors"])
        ]
        average_scores.sort(key=lambda x: x["average"], reverse=True)

        return Response(average_scores)



class GetGlobalAverageSimilarity(APIView):
    """
    List the average node similarity scores for all target-target pairs across all descriptors,
    filtered by the minimum number of descriptors in the average.
    """
    def get(self, request, *args, **kwargs):
        descriptors = {
            "mousepheno": "SIMILAR_MOUSEPHENO",
            "hgene": "SIMILAR_HGENE",
            "hprotein": "SIMILAR_HPROTEIN",
            "intact": "SIMILAR_INTACT",
            "pathway": "SIMILAR_PATHWAY",
            "reactome": "SIMILAR_REACTOME",
            "signor": "SIMILAR_SIGNOR",
            # "gwas": "SIMILAR_GWAS",
        }

        # Check if min_descriptors is in the requested path
        try:
            min_descriptors = self.kwargs['min_descriptors']
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Initialize empty defaultdict for storing results
        descriptor_results = defaultdict(lambda: {"total": 0, "count": 0, "descriptors": set()})

        for descriptor_type, relationship_type in descriptors.items():
            # Get similarity results from Neo4j using Cypher query
            results = db.cypher_query(
                f'''
                MATCH (n1:Target)-[r:{relationship_type}]-(n2:Target)
                WHERE n1 <> n2
                RETURN n1.symbol, n2.symbol, r.score
                '''
            )[0]
            print(f"{relationship_type} results pulled from Neo4j")

            # Calculate the sum, count, and descriptors for each target pair
            for row in results:
                target1, target2, similarity = row
                target_pair = tuple(sorted([target1, target2]))
                descriptor_results[target_pair]["total"] += similarity
                descriptor_results[target_pair]["count"] += 1
                descriptor_results[target_pair]["descriptors"].add(descriptor_type)
            
            print(f"{relationship_type} results processed")

        # Calculate the averages and sort results by average in descending order
        average_scores = [
            {
                "target1": target_pair[0],
                "target2": target_pair[1],
                "average": total / count,
                "descriptors": list(descriptors)
            }
            for target_pair, result in descriptor_results.items()
            if (total := result["total"]) and (count := result["count"]) and (descriptors := result["descriptors"]) and len(descriptors) >= min_descriptors
        ]
        average_scores.sort(key=lambda x: x["average"], reverse=True)

        return Response(average_scores)



# Upload one or more entities in a comma-separated file
@require_http_methods(["POST"])
def upload_csv(request):
    # Implement the functionality for uploading a CSV
    pass

# Return the content of a previously uploaded comma-separated file
@require_http_methods(["GET"])
def get_csv(request, file_id):
    # Implement the functionality for retrieving the content of a CSV
    pass

# Clear out the database
@csrf_exempt
@require_http_methods(["POST"])
def clear(request):
    # Implement the functionality for clearing out the database
    try:
        clear_neo4j_database()
        return HttpResponse('Neo4J DB cleared', status=200)

    except Exception as e:
        return HttpResponse('Internal Server Error', status=500)


# Initialize entities (all or of the specified type) from the OpenTargets store
@require_http_methods(["POST"])
def init_type(request, type_string=None):
    # Implement the functionality for initializing entities from the OpenTargets store
    pass

# Add a single gene entity to the database
@require_http_methods(["POST"])
def gene(request, id):
    # Implement the functionality for adding a single gene entity to the database
    pass


class Datasets(APIView):
    """
    Return an array of all known datasets (both active and inactive).
    """

    def get(self, request):
        # Retrieve all Dataset objects from the Neo4j database
        datasets = fetch_datasets()

        datasets = [{"name": item } for item in datasets]

        # Return the data as a JSON response
        return Response(datasets, status=status.HTTP_200_OK)

    """
    Modify the active status of one or more datasets
    """

    def post(self, request):
        # Parse the JSON request body
        try:
            datasets = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Modify the dataset status
        for dataset in datasets:
            dataset_name = dataset.get("dataset")
            enabled = dataset.get("enabled")
            if dataset_name and enabled is not None:
                update_dataset_status(dataset_name, bool(enabled))

        return JsonResponse({}, status=200)

# Return an array of adverse events associated with a specific target
class GetAdverseEventByTargetView(APIView):
    def get(self, request, target, ae=None):
        # Extract query parameters
        action_types = request.query_params.get('action_types')
        drug = request.query_params.get('drug')
        count = request.query_params.get('count')

        # Convert action_types to a list if provided
        if action_types:
            action_types = action_types.split(',')

        # Convert count to an integer if provided
        if count:
            count = int(count)

        # Call the helper function to get the results
        result = get_weights_by_target(target, ae, action_types, drug, count)

        # Return the result as a JSON response
        return Response(result, status=status.HTTP_200_OK)

# Return an array of targets associated with a specific adverse event
class GetTargetByAdverseEventView(APIView):
    def get(self, request, ae, target=None):
        # Extract query parameters
        action_types = request.query_params.get('action_types')
        drug = request.query_params.get('drug')
        count = request.query_params.get('count')

        # Convert action_types to a list if provided
        if action_types:
            action_types = action_types.split(',')

        # Convert count to an integer if provided
        if count:
            count = int(count)

        # Call the helper function to get the results
        result = get_weights_by_ae(ae, target, action_types, drug, count)

        # Return the result as a JSON response
        return Response(result, status=status.HTTP_200_OK)


# Return an array of weights of adverse events associated with a specific target
@require_http_methods(["GET"])
def get_weights_target_ae(request, target, ae):
    # Implement the functionality for returning an array of weights of adverse events associated with a specific target
    pass

# Return an array of Cytoscape entities representing paths from a target to one or all adverse events associated with it, optionally filtered by drug and action
@require_http_methods(["GET"])
def get_paths_target_ae_drug_view(request, target, ae=None, drug_id=None):
    # Implement the functionality for returning an array of Cytoscape entities representing paths from a target to adverse events
    pass

class GetAdverseEventTargetPath(APIView):
    """
    This view returns Cytoscape entities representing paths from a target to one or all adverse events,
    optionally filtered by adverse event, and drug_id.
    """
    def get(self, request, target_symbol, adverse_event=None, drug_id=None):
        # Get the list of action types from the request's query parameters, if any.
        actions = request.GET.getlist('action_types')
        actions = actions if actions else None
        
        # Get the count parameter from the request's query parameters, if any, and convert it to an integer.
        count = request.GET.get('count', None)
        if count:
            count = int(count)

        # Retrieve Cytoscape entities representing paths from a target to one or all adverse events.
        # The target, action types, adverse event, and drug_id are used as filters for the query.
        entities = get_paths_target_ae_drug(target_symbol, actions, adverse_event, drug_id, count)
        result = get_cytoscape_entities_as_json(entities)

        # Return the JSON representation of the resulting entities.
        return JsonResponse(result, safe=False)

class GetTargetAdverseEventPath(APIView):
    """
    This view returns Cytoscape entities representing paths from an adverse event to one or all targets,
    optionally filtered by target_symbol, and drug_id.
    """
    def get(self, request, adverse_event, target_symbol=None, drug_id=None):
        # Get the list of action types from the request's query parameters, if any.
        actions = request.GET.getlist('action_types')
        actions = actions if actions else None
        
        # Get the count parameter from the request's query parameters, if any, and convert it to an integer.
        count = request.GET.get('count', None)
        if count:
            count = int(count)

        # Retrieve Cytoscape entities representing paths from an adverse event to one or all targets.
        # The adverse event, action types, target_symbol, and drug_id are used as filters for the query.
        entities = get_paths_ae_target_drug(adverse_event, actions, target_symbol, drug_id, count)
        result = get_cytoscape_entities_as_json(entities)

        # Return the JSON representation of the resulting entities.
        return JsonResponse(result, safe=False)


    
class CountView(APIView):
    """
    CountView handles GET requests to return the count of a specific entity type.
    """

    def get(self, request, type_string, *args, **kwargs):
        try:
            num_entities = get_entity_count(type_string)
            
            return Response(num_entities, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class CountAllView(APIView):
    """
    CountAllView handles GET requests to return the count of all entity types and relationships.
    """

    def get(self, request, *args, **kwargs):

        try:
            counts = count_all_entities()

            counts = convert_array(counts)

            return Response(counts, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

""" Function to process array in to cleaner format for frontend"""
def convert_array(original_array):
    result_dict = {}
    for subarr in original_array:
        key, value = subarr
        result_dict[key] = value
    
    result_array = []
    for key, value in result_dict.items():
        result_array.append({"name": key.lower(), "count": value})
    
    return result_array


# Health check
@require_http_methods(["GET"])
def info(request):
    # Implement the functionality for a health check
    pass

class SuggestHintView(APIView):
    """
    SuggestHintView handles GET requests to return an array of suggested entities in response to a hint (beginning of the name)
    """

    def get(self, request, entity_type, hint, *args, **kwargs):
        try:
            match entity_type:
                case "target":
                    results_list = suggestion_by_hint_for_target(hint)
                
                case "adverse_event":
                    results_list = suggestion_by_hint_for_adverse_event(hint)
                
                case "disease":
                    results_list = suggestion_by_hint_for_disease(hint)

                case "drug":
                    results_list = suggestion_by_hint_for_drug(hint)

                case "mouse_phenotype":
                    results_list = suggestion_by_hint_for_mouse_phenotype(hint)

                case "pathway":
                    results_list = suggestion_by_hint_for_pathway(hint)
                
                case _:
                    return JsonResponse({}, status=400)

            return JsonResponse(results_list, safe=False, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)




# Return an array of all actions in the database
@require_http_methods(["GET"])
def actions(request, target=None):
    # Implement the functionality for returning an array of all actions or actions for the specified target
    pass
 