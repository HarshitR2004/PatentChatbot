from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('/users/login/')

urlpatterns = [
    path('', redirect_to_login, name='home'),  # Redirect root to login
    path('admin/', admin.site.urls),
    path('users/', include('Users.urls')),
    path('documents/', include('documents.urls')),
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
