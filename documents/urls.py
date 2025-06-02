from django.urls import path
from . import views

urlpatterns = [
    # Route for rendering the documents HTML page
    path('', views.show_documents, name='show_documents'),
    
    # Route for the API to list all documents
    path('api/documents/', views.DocumentsListView.as_view(), name='documents-list'),
]
