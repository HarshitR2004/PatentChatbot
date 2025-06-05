from django.http import StreamingHttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Users.models import Users
from usersession.models import userSession
from chat.models import Chat
from django.shortcuts import render
import json
import time
import ollama

client = ollama.Client()
model = "gemma3" 

def generate_rag_response(query: str) -> str:
    """
    Generates a concise RAG response in 2 to 3 lines using a system prompt and temperature setting.
    """
    try:
        response = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": "You are a patent expert assistant. Answer patent-related questions concisely in just 2 to 3 lines. Focus on practical, accurate information"},
                {"role": "user", "content": query}
            ],
        )
        
        return response['message']['content'] if 'message' in response else "No response generated."
    except Exception as e:
        return f"Sorry, I encountered an error while processing your query: {str(e)}"

def generate_rag_response_stream(query: str):
    """
    Generates streaming RAG response using Ollama with streaming support
    """
    try:
        stream = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": "You are a patent expert assistant. Answer patent-related questions concisely in just 2 to 3 lines. Focus on practical, accurate information"},
                {"role": "user", "content": query}
            ],
            stream=True,
        )
        
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']
                
    except Exception as e:
        yield f"Sorry, I encountered an error while processing your query: {str(e)}"

class ChatAPIView(APIView):
    def post(self, request):
        query = request.data.get('query')
        session_id = request.data.get('session_id')
        user_id = request.user.id
        test_mode = request.data.get('test', False)

        if not query:
            return Response({'error': 'A query is required'}, status=status.HTTP_400_BAD_REQUEST)

        if test_mode:
            def generate_test_stream():
                # Send start event
                yield f"data: {json.dumps({'event': 'start', 'message': 'Generating response using AI...'})}\n\n"
                
                accumulated_text = ""
                token_count = 0
                
                try:
                    # Use Ollama streaming
                    for chunk in generate_rag_response_stream(query):
                        if chunk:  
                            accumulated_text += chunk
                            token_count += 1
                            
                            chunk_data = {
                                'event': 'token',
                                'token': chunk,
                                'accumulated_text': accumulated_text,
                                'token_count': token_count,
                                'is_complete': False
                            }
                            
                            yield f"data: {json.dumps(chunk_data)}\n\n"
                            time.sleep(0.02)  # Small delay
                
                except Exception as e:
                    error_data = {
                        'event': 'error',
                        'message': f"Error generating response: {str(e)}",
                        'is_complete': True
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"
                    return
                
                # Send completion event
                final_data = {
                    'event': 'complete',
                    'full_response': accumulated_text,
                    'total_tokens': token_count,
                    'is_complete': True
                }
                yield f"data: {json.dumps(final_data)}\n\n"
            
            response = StreamingHttpResponse(
                generate_test_stream(),
                content_type='text/event-stream'
            )
            response['Cache-Control'] = 'no-cache'
            response['Access-Control-Allow-Origin'] = '*'
            return response

        # Normal mode: Streaming with database save
        # Validate session first
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

        def generate_normal_stream():
            start_time = timezone.now()
            
            # Send start event with session info
            yield f"data: {json.dumps({'event': 'start', 'session_id': session.session_id, 'message': 'Generating AI response...'})}\n\n"
            
            accumulated_text = ""
            token_count = 0
            
            try:
                # Use Ollama streaming
                for chunk in generate_rag_response_stream(query):
                    if chunk:  
                        accumulated_text += chunk
                        token_count += 1
                        
                        chunk_data = {
                            'event': 'token',
                            'token': chunk,
                            'accumulated_text': accumulated_text,
                            'session_id': session.session_id,
                            'token_count': token_count,
                            'is_complete': False
                        }
                        
                        yield f"data: {json.dumps(chunk_data)}\n\n"
                        time.sleep(0.02)  # Small delay
                        
            except Exception as e:
                error_data = {
                    'event': 'error',
                    'session_id': session.session_id,
                    'message': f"Error generating response: {str(e)}",
                    'is_complete': True
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                return
            
            # Save to database after streaming is complete
            end_time = timezone.now()
            
            latest_chat = Chat.objects.order_by('-chatID').first()
            new_chat_id = (latest_chat.chatID + 1) if latest_chat else 1
            
            try:
                chat = Chat.objects.create(
                    chatID=new_chat_id,
                    queryText=query,
                    responseText=accumulated_text,
                    session_id=session,
                    startTime=start_time,
                    endTime=end_time,
                )
                
                # Send completion event with chat info
                final_data = {
                    'event': 'complete',
                    'full_response': accumulated_text,
                    'total_tokens': token_count,
                    'chat_id': chat.chatID,
                    'session_id': session.session_id,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'is_complete': True
                }
                yield f"data: {json.dumps(final_data)}\n\n"
                
            except Exception as e:
                error_data = {
                    'event': 'error',
                    'session_id': session.session_id,
                    'message': f"Error saving chat: {str(e)}",
                    'is_complete': True
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        response = StreamingHttpResponse(
            generate_normal_stream(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['Access-Control-Allow-Origin'] = '*'
        return response

class SessionChatsAPIView(APIView):
    def get(self, request, session_id):
        try:
            session = userSession.objects.get(pk=session_id)
            chats = Chat.objects.filter(session_id=session).order_by('startTime')
            
            chat_data = []
            for chat in chats:
                chat_data.append({
                    'chat_id': chat.chatID,
                    'query': chat.queryText,
                    'response': chat.responseText,
                    'start_time': chat.startTime.isoformat(),
                    'end_time': chat.endTime.isoformat() if chat.endTime else None
                })
            
            return Response({
                'session_id': session_id,
                'chats': chat_data
            }, status=status.HTTP_200_OK)
            
        except userSession.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


def chat_page(request):
    """
    Render the chat page template.
    """
    return render(request, 'chat/chat.html', {
        'user': request.user
    })





