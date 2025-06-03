from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_documents, name='show_documents'),
    path('<int:docid>/', views.view_document, name='view_document'),
]
