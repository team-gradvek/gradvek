from django.urls import path

from . import views

app_name = "search"

urlpatterns =  [
    path("api/descriptors", views.DescriptorListView.as_view(), name = "descriptors"),
    path("api/targets", views.TargetListView.as_view(), name = "targets"),
    path("api/adverse-events", views.AdverseEventListView.as_view(), name = "adverse-events"),

]