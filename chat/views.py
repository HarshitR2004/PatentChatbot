from django.shortcuts import render
from .models import Chat


# Create your views here.
def chat(request):
   return render(request, 'chat/chat.html')
    
    

    
    
    