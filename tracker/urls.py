from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("issues/", views.index, name="issues"),
    path("issues/<int:issue_id>/update", views.update_issue, name="update_issue"),
    path("issues/create/", views.create_issue, name="create_issue"),
    path("issues/pdf/", views.generate_pdf, name="pdf_generation"),
    path('issues/filter', views.IssueFilterView.as_view(), name='issue_filter'),
]