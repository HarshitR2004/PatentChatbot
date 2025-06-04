from django.urls import path
from . import views



app_name = 'users'

urlpatterns = [
    # Web pages
    path('login/', views.login_view, name='login-page'),
    path('register/', views.register_view, name='register-page'), 
    
    # API endpoints
    path('api/login/', views.login_api, name='login-api'),
    path('api/register/', views.register_api, name='register-api'),
    path('api/logout/', views.logout_api, name='logout-api'),
]