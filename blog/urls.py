from django.contrib import admin
from django.urls import re_path
from blog import views

app_name = "request_demo"

urlpatterns = [
    re_path(r"^index/$", views.index, name="index"),
]
