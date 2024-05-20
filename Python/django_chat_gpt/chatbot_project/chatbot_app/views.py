import requests
from openai import AzureOpenAI

from django.shortcuts import render, redirect
from django.conf import settings

from .models import Message


def chat_view(request):
    messages = Message.objects.all()
    return render(request, 'chat.html', {'messages': messages})

def add_conversation(request):
    
    user_message = request.POST.get('message')
    bot_message = get_ai_response(user_message)
    Message.objects.create(user_message=user_message, bot_message=bot_message)
    messages = Message.objects.all()
    return render(request, 'partials/_chat_box.html', {'messages': messages})

def clear_chat(request):
    Message.objects.all().delete()
    messages = Message.objects.all()
    return redirect('chat_view')

def get_ai_response(user_input: str) -> str:
    # get all messages from the database
    messages = get_existing_messages()
    messages.append({"role": "user", "content": f"{user_input}"})
    
    # initialise the client
    client = AzureOpenAI(
    api_key=settings.OPEN_AI_API_KEY,  
    api_version="2024-02-01",
    azure_endpoint = settings.OPEN_AI_END_POINT
    )
    
    # deployment_name="gpt4" 
    deployment_name= settings.OPEN_AI_DEPLOYMENT_NAME
    
    response = client.chat.completions.create(model=deployment_name, messages=messages)

    ai_message = response.choices[0].message.content
    return ai_message


def get_existing_messages() -> list:
    """
    Get all messages from the database and format them for the API.
    """
    formatted_messages = []

    for message in Message.objects.values('user_message', 'bot_message'):
        formatted_messages.append({"role": "user", "content": message['user_message']})
        formatted_messages.append({"role": "assistant", "content": message['bot_message']})

    return formatted_messages