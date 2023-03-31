from django.urls import path

from . import views

app_name = "search"

urlpatterns =  [
    path("api/descriptors", views.DescriptorListView.as_view(), name = "descriptors"),

]