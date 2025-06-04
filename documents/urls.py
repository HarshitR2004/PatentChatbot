from django.urls import path
from . import views

urlpatterns = [
    # Web pages
    path('', views.document_list, name='document-list'),
    path('viewer/<int:docid>/', views.document_viewer, name='document-viewer'),
    
    # API endpoints  
    path('api/', views.DocumentListAPIView.as_view(), name='document-list-api'),
    path('api/upload/', views.document_upload, name='document-upload'),
    path('api/delete/<int:docid>/', views.document_delete, name='document-delete'),
]
