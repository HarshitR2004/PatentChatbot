from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404,render
from .models import Documents
from .serializers import DocumentsSerializer

def view_document(request, docid):
    document = get_object_or_404(Documents, docid=docid)
    return render(request, 'documents/view_document.html', {'document': document})


class DocumentFileDetailsAPIView(APIView):
    def get(self, request, docid):
        document = get_object_or_404(Documents, docid=docid)
        serializer = DocumentsSerializer(document)
        return Response(serializer.data)
