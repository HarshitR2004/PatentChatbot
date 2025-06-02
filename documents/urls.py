from django.urls import path
from . import views

urlpatterns = [
    # Route for rendering the documents HTML page
    path('', views.show_documents, name='show_documents'),
    
    # Route for the API to list all documents and create a new document
    path('api/documents/', views.DocumentsListView.as_view(), name='documents-list'),
    
    # Route for the API to retrieve, update, or delete a specific document
    path('api/documents/<int:docid>/', views.DocumentsDetailView.as_view(), name='document-detail'),
]
