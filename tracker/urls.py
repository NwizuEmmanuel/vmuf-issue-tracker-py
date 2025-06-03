from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("issues/", views.index, name="issues"),
    path("issues/<int:issue_id>/update", views.update_issue, name="update_issue"),
    path("issues/create/", views.create_issue, name="create_issue"),
    path("issues/delete", views.delete_issue, name="delete_issue"),
]