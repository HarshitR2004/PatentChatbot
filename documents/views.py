from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Documents
from .serializers import DocumentsSerializer

# Create your views here.
def show_documents(request):
    return render(request, 'documents/documents.html')

class DocumentsListView(APIView):
    def get(self, request):
        # Fetch all documents from the database
        documents = Documents.objects.all()
        # Serialize the data into JSON format
        serializer = DocumentsSerializer(documents, many=True)
        # Return the serialized data as a response
        return Response(serializer.data)