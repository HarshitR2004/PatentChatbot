from django.shortcuts import render

# Create your views here.
def show_documents(request):
    return render(request, 'documents/documents.html')