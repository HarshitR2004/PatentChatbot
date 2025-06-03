from django.shortcuts import get_object_or_404, render
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.paginator import Paginator
from .models import Documents
from .serializers import DocumentSerializer

class DocumentListAPIView(APIView):
    """
    GET: List all documents with pagination only
    """
    
    def get(self, request):
        """Get list of documents with pagination"""
        try:
            documents = Documents.objects.all().order_by('-uploadTime')
            
            # Pagination
            page = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 10)
            
            paginator = Paginator(documents, page_size)
            page_obj = paginator.get_page(page)
            
            serializer = DocumentSerializer(
                page_obj.object_list, 
                many=True, 
                context={'request': request}
            )
            
            return Response({
                'documents': serializer.data,
                'pagination': {
                    'current_page': page_obj.number,
                    'total_pages': paginator.num_pages,
                    'total_documents': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Failed to retrieve documents: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def document_list(request):
    """Render document list page"""
    return render(request, 'documents/document_list.html')

def document_viewer(request, docid):
    """Render document details and PDF viewer"""
    document = get_object_or_404(Documents, docid=docid)
    return render(request, 'documents/document_viewer.html', {
        'document': document
    })


