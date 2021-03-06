from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create", views.create, name="create"),
    path("<str:id>", views.info, name="info"),
    path("delete/<str:id>", views.delete, name="delete")
]
