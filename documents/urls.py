from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_documents, name='show_documents'),  # HTML page
    path('view/<int:docid>/', views.view_document, name='view-document'),
    path('api/documents/<int:docid>/', views.DocumentFileDetailsAPIView.as_view(), name='document-file-details'),  # single doc JSON
]
