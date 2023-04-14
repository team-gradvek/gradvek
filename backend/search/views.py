from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Descriptor, Action
from .serializers import DescriptorSerializer, ActionsSerializer


from .utils import (
    fetch_actions,
    fetch_datasets,
)

# Collect Descriptors list from sqlite and format it to send back
#  to next.js


class DescriptorListView(generics.ListAPIView):
    queryset = Descriptor.objects.all()
    serializer_class = DescriptorSerializer

# class ActionListView(generics.ListAPIView):
#     actions = fetch_actions()
#     # queryset = fetch_actions()
#     # queryset = Action.objects.all()
#     serializer_class = ActionsSerializer(actions, many=True)

class GetActions(APIView):
    def get(self, request):
        actions = fetch_actions()
        data = { 
            'response': {
                'status': '200',
                'data': actions,
            },
        }
        return Response(data)


# Trying to copy paths from gradvek 1.0

#Upload one or more entities in a comma-separated file
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
@require_http_methods(["POST"])
def clear(request):
    # Implement the functionality for clearing out the database
    pass

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

class DatasetList(APIView):
    """
    Return an array of all known datasets (both active and inactive).
    """

    def get(self, request):
        # Retrieve all Dataset objects from the Neo4j database
        datasets = fetch_datasets()

        # Return the data as a JSON response
        return Response(datasets, status=status.HTTP_200_OK)
    

# Modify the active status of one or more datasets
@require_http_methods(["POST"])
def enable_datasets(request):
    # Implement the functionality for modifying the active status of one or more datasets
    pass

# Return an array of adverse events associated with a specific target, optionally filtered by action
@require_http_methods(["GET"])
def get_adverse_event(request, target):
    # Implement the functionality for returning an array of adverse events associated with a specific target
    pass

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

# Return an array of Cytoscape entities representing paths from a target to one or all adverse events associated with it, optionally filtered by drug and action
@require_http_methods(["GET"])
def count(request, type_string):
    # Implement the functionality for counting entities by type
    pass

# Health check
@require_http_methods(["GET"])
def info(request):
    # Implement the functionality for a health check
    pass

# Return an array of suggested entities in response to a hint (beginning of the name)
@require_http_methods(["GET"])
def suggest_hint(request, hint):
    # Implement the functionality for returning an array of suggested entities in response to a hint
    pass

# Return an array of all actions in the database
@require_http_methods(["GET"])
def actions(request, target=None):
    # Implement the functionality for returning an array of all actions or actions for the specified target
    pass
