from django.urls import path
from . import views

urlpatterns = [
    path('view/<int:docid>/', views.view_document, name='view-document'), # HTML page
    path('api/documents/<int:docid>/', views.DocumentFileDetailsAPIView.as_view(), name='document-file-details'),  # single doc JSON
]
