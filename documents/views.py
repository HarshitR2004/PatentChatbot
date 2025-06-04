from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator
from .models import Documents
from .serializers import DocumentSerializer, DocumentUploadSerializer
import os

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

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def document_upload(request):
    """Handle document upload via API"""
    try:
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save()
            response_serializer = DocumentSerializer(document)
            return Response({
                'success': True,
                'message': 'Document uploaded successfully',
                'document': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['DELETE'])
def document_delete(request, docid):
    """Handle document deletion via API"""
    try:
        document = get_object_or_404(Documents, docid=docid)
        document_info = {
            'docid': document.docid,
            'patentNumber': document.patentNumber,
        }
        if document.documentPath and os.path.isfile(document.documentPath.path):
            try:
                os.remove(document.documentPath.path)
            except Exception as e:
                return Response({
                    'success': False,
                    'error': f'Failed to delete file: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        document.delete()
        return Response({
            'success': True,
            'message': 'Document deleted successfully',
            'document': document_info
        }, status=status.HTTP_200_OK)
    except Documents.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Document not found'
        }, status=status.HTTP_404_NOT_FOUND)
    