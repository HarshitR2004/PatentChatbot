from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from .models import Documents
from .serializers import DocumentsSerializer

# HTML page rendering view
def show_documents(request):
    """Render the documents.html page."""
    return render(request, 'documents/documents.html')

# API to list all documents and create a new document
class DocumentsListView(APIView):
    """Handle GET and POST requests for the Documents list."""
    
    def get(self, request):
        """Retrieve all documents."""
        documents = Documents.objects.all()
        serializer = DocumentsSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new document."""
        serializer = DocumentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to handle individual document operations
class DocumentsDetailView(APIView):
    """Handle GET, PUT, and DELETE requests for a specific Document."""
    
    def get_object(self, docid):
        """Retrieve a document by its ID or raise 404."""
        return get_object_or_404(Documents, docid=docid)

    def get(self, request, docid):
        """Retrieve a specific document."""
        document = self.get_object(docid)
        serializer = DocumentsSerializer(document)
        return Response(serializer.data)

    def put(self, request, docid):
        """Update a specific document."""
        document = self.get_object(docid)
        serializer = DocumentsSerializer(document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, docid):
        """Delete a specific document."""
        document = self.get_object(docid)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
