from .views import (
    CountAllView,
    GetActions,
    Datasets,
    GetAdverseEventTargetPath,
    GetAverageSimilarity,
    GetGlobalAverageSimilarity,
    # GetGwas,
    # GetHGene,
    # GetHProtein,
    # GetIntact,
    # GetPathway,
    # GetReactome,
    # GetSignor,
    GetTargetAdverseEventPath,
    GetTargetByAdverseEventView,
    GetWeightedAverageSimilarity,
    RoutesListAPIView,
    CountView,
    GetAdverseEventByTargetView,
    # GetPheno,
    SuggestHintView,
    GetSimilarity

)
from django.urls import path

from . import views


app_name = "search"


urlpatterns = [

    # path('api/pheno/<str:target>/', GetPheno.as_view(), name='pheno'),
    # path('api/gwas/<str:target>/', GetGwas.as_view(), name='gwas'),
    # path('api/hgene/<str:target>/', GetHGene.as_view(), name='hgene'),
    # path('api/hprotein/<str:target>/', GetHProtein.as_view(), name='hprotein'),
    # path('api/intact/<str:target>/', GetIntact.as_view(), name='intact'),
    # path('api/pathway/<str:target>/', GetPathway.as_view(), name='pathway'),
    # path('api/reactome/<str:target>/', GetReactome.as_view(), name='reactome'),
    # path('api/signor/<str:target>/', GetSignor.as_view(), name='signor'),

    # Return the list of routes in the Django site
    path('api/routes/', RoutesListAPIView.as_view(), name='api-routes-list'),
    
    # Return an array of actions for the specified target
    path("api/actions/", GetActions.as_view(), name='get_actions'),
    path('api/actions/<str:target>/', GetActions.as_view(), name='get_actions_target'),

    path("api/descriptors", views.DescriptorListView.as_view(), name="descriptors"),

    # Return list of all node similarity scores associated to a target
    path('api/similarity/<str:descriptor>/<str:target>/', GetSimilarity.as_view(), name='similarity'),
    path('api/average_similarity/<str:target>/', GetAverageSimilarity.as_view(), name='average_similarity'),
    path('api/weighted_average_similarity/<str:target>/', GetWeightedAverageSimilarity.as_view(), name='weighted_average_similarity'),
    path('api/global_average_similarity/<int:min_descriptors>/', GetGlobalAverageSimilarity.as_view(), name='global_average_similarity'),


    # Upload one or more entities in a comma-separated file
    path('api/csv/', views.upload_csv, name='upload_csv'),

    # Return the content of a previously uploaded comma-separated file
    path('api/csv/<str:file_id>/', views.get_csv, name='get_csv'),

    # Clear out the database
    path('api/clear/', views.clear, name='clear'),

    # Initialize entities (all or of the specified type) from the OpenTargets store
    path('api/init/', views.init_type, name='init_all'),
    path('api/init/<str:type_string>/', views.init_type, name='init_type'),

    # Add a single gene entity to the database
    path('api/gene/<str:id>/', views.gene, name='gene'),

    # GET: Return an array of all known datasets (both active and inactive)
    # POST: Modify the active status of one or more datasets
    path('api/datasets/', Datasets.as_view(), name='datasets'),

    # This route returns an array of adverse events associated with a specific target, optionally filtered by action types. It requires the drug target symbol as a path parameter
    # target: Drug Symbol
    path('api/weight/<str:target>/', GetAdverseEventByTargetView.as_view(), name='get_adverse_event_weights_from_ae'),

    # This route returns an array of weights (log likelihood ratios) of adverse events associated with a specific target. It requires the drug target symbol and adverse event ID (meddraId) as path parameters.
    # target: Drug Symbol, ae: meddraId
    path('api/weight/<str:target>/<str:ae>/', GetAdverseEventByTargetView.as_view(), name='get_weights_target_ae'),

    # This route returns an array of targets associated with a specific adverse event, optionally filtered by action types. It requires the meddraId as a path parameter
    # target: ae: meddraId
    path('api/ae-weight/<str:ae>/', GetTargetByAdverseEventView.as_view(), name='get_target_weights_from_ae'),

    # This route returns an array of weights (log likelihood ratios) of and adverse events association for several targets. It requires the adverse event ID (meddraId) and drug target symbol as path parameters.
    # target: Drug Symbol, ae: meddraId
    path('api/ae-weight/<str:ae>/<str:target>/', GetTargetByAdverseEventView.as_view(), name='get_weights_ae_target'),

    # These paths define API routes for querying paths from a target to one or all adverse events
    # associated with it, optionally filtered by drug and action.
    # target_symbol: Symbol, adverse_event: meddraId, drug_id: chemblId
    path('api/ae/path/<str:target_symbol>/', GetAdverseEventTargetPath.as_view(), name='get_paths_target'),
    path('api/ae/path/<str:target_symbol>/<str:adverse_event>/', GetAdverseEventTargetPath.as_view(), name='get_paths_target_ae'),
    path('api/ae/path/<str:target_symbol>/<str:adverse_event>/<str:drug_id>/', GetAdverseEventTargetPath.as_view(), name='get_paths_target_ae_drug'),

    # These paths define API routes for querying paths from an adverse event to one or all targets
    # associated with it, optionally filtered by drug and action.
    # adverse_event: meddraId, target_symbol: Symbol, drug_id: chemblId
    path('api/target/path/<str:adverse_event>/', GetTargetAdverseEventPath.as_view(), name='get_paths_ae'),
    path('api/target/path/<str:adverse_event>/<str:target_symbol>/', GetTargetAdverseEventPath.as_view(), name='get_paths_ae_target'),
    path('api/target/path/<str:adverse_event>/<str:target_symbol>/<str:drug_id>/', GetTargetAdverseEventPath.as_view(), name='get_paths_ae_target_drug'),

    # Return an array of Cytoscape entities representing paths from a target to one or all adverse events associated with it, optionally filtered by drug and action
    path('api/count/', CountAllView.as_view(), name='count_all'),
#     path('api/count/', CountView.as_view(), name='count_all'),
    path('api/count/<str:type_string>/', CountView.as_view(), name='count_entity'),

    # Health check
    path('api/info/', views.info, name='info'),

    # Return an array of suggested entities in response to a hint (beginning of the name)
    path('api/suggest/<str:entity_type>/<str:hint>/', SuggestHintView.as_view(), name='suggest_hint'),


    # Return an array of actions for the specified target
    path('api/actions/<str:target>/', views.actions, name='actions_target'),


    # # Clear out the database
    path('api/clear/', views.clear, name='clear'),

    # # Initialize entities (all or of the specified type) from the OpenTargets store
    # path('api/init/', views.init_type, name='init_all'),
    # path('api/init/<str:type_string>/', views.init_type, name='init_type'),

    # # Add a single gene entity to the database
    # path('api/gene/<str:id>/', views.gene, name='gene'),

    # # Return an array of all known datasets (both active and inactive)
    # path('api/datasets/', views.datasets, name='datasets'),

    # # Modify the active status of one or more datasets
    # path('api/enable_datasets/', views.enable_datasets, name='enable_datasets'),

    # # Return an array of adverse events associated with a specific target, optionally filtered by action
    # path('api/weight/<str:target>/', views.get_adverse_event, name='get_adverse_event'),

    # # Return an array of weights of adverse events associated with a specific target, optionally filtered by action
    # path('api/weight/<str:target>/<str:ae>/', views.get_weights_target_ae, name='get_weights_target_ae'),

    # # Return an array of Cytoscape entities representing paths from a target to one or all adverse events associated with it, optionally filtered by drug and action
    # path('api/ae/path/<str:target>/', views.get_paths_target_ae_drug_view, name='get_paths_target_ae'),
    # path('api/ae/path/<str:target>/<str:ae>/', views.get_paths_target_ae_drug_view, name='get_paths_target_ae_ae'),
    # path('api/ae/path/<str:target>/<str:ae>/<str:drug_id>/', views.get_paths_target_ae_drug_view, name='get_paths_target_ae_drug'),

    # # Return an array of Cytoscape entities representing paths from a target to one or all adverse events associated with it, optionally filtered by drug and action
    # path('api/count/<str:type_string>/', views.count, name='count'),

    # # Health check
    # path('api/info/', views.info, name='info'),

    # # Return an array of suggested entities in response to a hint (beginning of the name)
    # path('api/suggest/<str:hint>/', views.suggest_hint, name='suggest_hint'),

    # # Return an array of all actions in the database
    # path('api/actions/', views.actions, name='actions'),

    # # Return an array of actions for the specified target
    # path('api/actions/<str:target>/', views.actions, name='actions_target')

    # # TODO Add some paths for retrieving similarity information?

]
