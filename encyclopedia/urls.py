from django.urls import path

from . import views

# app_name = "enc"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/error", views.error, name="error"),
    path("wiki/add", views.add, name="add"),
    path("wiki/add/<str:title>", views.add, name="add"),
    path("wiki/random", views.random_entry, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("<str:title>", views.entry, name="e_entry")
]
