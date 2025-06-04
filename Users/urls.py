from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # API endpoints
    path('api/login/', views.login_api, name='login_api'),
    path('api/register/', views.register_api, name='register_api'),
    path('api/logout/', views.logout_api, name='logout_api'),
    path('api/profile/', views.profile_api, name='profile_api'),
    path('api/users/', views.users_list_api, name='users_list_api'),
    # HTML pages
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
]