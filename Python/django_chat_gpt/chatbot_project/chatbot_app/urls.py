from django.urls import path
from .views import chat_view, clear_chat, add_conversation

urlpatterns = [
    path('', chat_view, name='chat_view'),
    path('clear_chat', clear_chat, name='clear_chat'),
    path('add_conversation', add_conversation, name='add_conversation'),
]