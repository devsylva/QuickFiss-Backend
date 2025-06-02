from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.HelloWorldView.as_view(), name="hello_world"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("services/", views.ServiceListView.as_view(), name="service_list"),
]