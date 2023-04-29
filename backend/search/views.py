import csv
import json
import os
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

from .models import Descriptor, Action
from .serializers import DescriptorSerializer, ActionsSerializer


from .utils import (
    count_all_entities,
    fetch_actions,
    fetch_datasets,
    get_all_routes,
    get_cytoscape_entities_as_json,
    get_entity_count,
    get_paths_target_ae_drug,
    get_weights_by_target,
    update_dataset_status,
    clear_neo4j_database,
    fetch_pheno,
    suggestion_by_hint_for_target,
    suggestion_by_hint_for_adverse_event,
    suggestion_by_hint_for_disease,
    suggestion_by_hint_for_drug,
    suggestion_by_hint_for_mouse_phenotype,
    suggestion_by_hint_for_pathway,

)

from .csv_service import (
    parse_and_load_csv_file
)

# API view to list all routes in the Django site
class RoutesListAPIView(generics.GenericAPIView):
    # Override the get_queryset method to return None, as we don't deal with a queryset
    def get_queryset(self):
        return None
    # Override the GET method to return the list of routes
    def get(self, request, *args, **kwargs):
        resolver = get_resolver(None)  # Get the project's URL resolver
        # Extract all routes from the URL patterns
        routes = get_all_routes(resolver.url_patterns)
        return Response(routes)  # Return the list of routes as a JSON response

# Collect Descriptors list from sqlite and format it to send back
#  to next.js
class DescriptorListView(generics.ListAPIView):
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
        data = {
            'response': {
                'status': '200',
                'data': actions,
            },
        }
        return Response(data)
 
class GetPheno(APIView):
    """
     Return most similar targets - 
     Mouse Phenotype similarity descending order
    """
    def get(self, request,  *args, **kwargs):

        # Check if a target is in the requested path
        try: 
            target = self.kwargs["target"]
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        # Get cypher query results
        pheno = fetch_pheno(target)

        # Return the result as a JSON response
        return Response(pheno, status=status.HTTP_200_OK)  

# Return an array of actions for the specified target
#actions/{target}


# Trying to copy paths from gradvek 1.0

# CSVVVVV
# Upload one or more entities in a comma-separated file
@csrf_exempt
@require_http_methods(["POST"])
def upload_csv(request):
    # Implement the functionality for uploading a CSV
    filename = "drug_to_ae.csv"
    filepath = os.path.join(os.getcwd(), filename)

    # Open the CSV file and pass it to another function for processing
    with open(filepath, "r") as csv_file:
        reader = csv.reader(csv_file)
        parse_and_load_csv_file(reader)

    return HttpResponse('method completed', status=200)


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
        data = {
            'response': {
                'status': '200',
                'data': datasets,
            },
        }
        # Return the data as a JSON response
        return Response(data)

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

# Return an array of adverse events associated with a specific target, optionally filtered by action
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


# Return an array of weights of adverse events associated with a specific target, optionally filtered by action
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
    # This function finds paths between the given target, adverse events, and drugs. 
    # It returns the results as a list of paths.
    def get(self, request, target, ae=None, drug_id=None):
        # Get the list of action types from the request's query parameters, if any.
        actions = request.GET.getlist('action_types')
        actions = actions if actions else None
        
        # Get the count parameter from the request's query parameters, if any, and convert it to an integer.
        count = request.GET.get('count', None)
        if count:
            count = int(count)

        # Retrieve Cytoscape entities representing paths from a target to one or all adverse events.
        # The target, action types, adverse event, and drug_id are used as filters for the query.
        entities = get_paths_target_ae_drug(target, actions, ae, drug_id, count)
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
            return Response({"counts": counts}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



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
 