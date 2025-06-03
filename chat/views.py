from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.utils import timezone
from .models import Chat
from usersession.models import userSession
from .serializers import ChatSerializer
from Users.models import Users
from django.shortcuts import render



def generate_rag_response(query):
    """
    Placeholder for RAG response generation logic
    In the future, this will integrate with RAG pipeline
    """
    dummy_data = {
        'what is a patent': 'A patent is a form of intellectual property that gives the patent holder exclusive rights to an invention for a certain period of time.',
        'how do i file a patent': 'To file a patent, you need to prepare a detailed description of your invention, including claims, drawings, and an abstract. Then, submit it to the relevant patent office.',
        'what are the types of patents': 'There are three main types of patents: utility patents, design patents, and plant patents.',
        'what is the duration of a patent': 'The duration of a patent typically lasts for 20 years from the filing date, but this can vary by jurisdiction and type of patent.',
    }
    
    # Match query against dummy data to simulate RAG response
    query_lower = query.lower().strip()
    for key, response in dummy_data.items():
        if key in query_lower:
            return response
    
    return "No response found for the given query."

class ChatAPIView(APIView):
    def post(self, request):
        query = request.data.get('query')
        session_id = request.data.get('session_id')
        user_id = request.user.get_UserID()
        test_mode = request.data.get('test', False)
        
        if test_mode:
            response_text = generate_rag_response(query)
            return Response({'responseText': response_text}, status=status.HTTP_200_OK)

        if not query:
            return Response({'error': 'A query is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not session_id:
            if not user_id:
                return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = Users.objects.get(pk=user_id)
            except Users.DoesNotExist:
                return Response({"error": "Invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)

            session = userSession.objects.create(user_id=user)
        else:
            try:
                session = userSession.objects.get(pk=session_id)
            except userSession.DoesNotExist:
                return Response({"error": "Invalid session_id"}, status=status.HTTP_400_BAD_REQUEST)
            

        # Generate response
        start_time = timezone.now()
        response_text = generate_rag_response(query)
        endTime = timezone.now()
        
        latest_chat = Chat.objects.order_by('-chatID').first()
        new_chat_id = (latest_chat.chatID + 1) if latest_chat else 1 

        chat = Chat.objects.create(
            chatID=new_chat_id,
            queryText=query,
            responseText=response_text,
            session_id=session,
            startTime=start_time,
            endTime=endTime,
        )

        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SessionChatsAPIView(ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        try:
            session = userSession.objects.get(session_id=session_id)
        except userSession.DoesNotExist:
            return Chat.objects.none()
        
        return Chat.objects.filter(session_id=session).order_by('created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'error': 'Invalid session_id or no chats found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)







