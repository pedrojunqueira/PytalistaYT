## Django Chat GPT App

### Step 1: Create a Python Virtual Environment and activate it
```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 2: Create a requirement.txt file in the root directory with the following content
```bash
annotated-types==0.6.0
anyio==4.3.0
asgiref==3.8.1
certifi==2024.2.2
charset-normalizer==3.3.2
distro==1.9.0
Django==5.0.3
django-environ==0.11.2
h11==0.14.0
httpcore==1.0.4
httpx==0.27.0
idna==3.6
openai==1.14.2
pydantic==2.6.4
pydantic_core==2.16.3
requests==2.31.0
sniffio==1.3.1
sqlparse==0.4.4
tqdm==4.66.2
typing_extensions==4.10.0
urllib3==2.2.1
```


### Step 3: Install Django and other required packages
```bash
pip install -r requirements.txt
```

### Step 4: Create a Django project
```bash
django-admin startproject chatbot_project
```

### Step 5: Create a Django app
```bash
cd chatbot_project
python manage.py startapp chatbot_app
```

### Step 6: add chachat_app to INSTALLED_APPS in chatbot_project/settings.py
```python
INSTALLED_APPS = [
    ...
    'chatbot_app',
]
```

### Step 7: Add your Azure OpenAI credentials to the .env file

create a file in the root directory of the project called .env

with the following content

```bash
OPEN_AI_END_POINT=https://<YourOpenAPIName>.openai.azure.com/
OPEN_AI_API_KEY=<YourAPIKEY>
OPEN_AI_DEPLOYEMENT_NAME=<YourDeploymentName>
```

### Step 8: Add environment variables to settings.py
```python
# add at the top of the file just after from pathlib import Path (about line 14)
import environ
import os

## this part add after the line  BASE_DIR = Path(__file__).resolve().parent.parent
# initialise env
env = environ.Env()

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

OPEN_AI_END_POINT = env('OPEN_AI_END_POINT')
OPEN_AI_API_KEY = env('OPEN_AI_API_KEY')
OPEN_AI_DEPLOYMENT_NAME = env('OPEN_AI_DEPLOYMENT_NAME')
```

### Step 9: Create a model for storing chat messages in chatbot_app/models.py
```python
from django.db import models


class Message(models.Model):
        user_message = models.TextField()
        bot_message = models.TextField()    
        timestamp = models.DateTimeField(auto_now_add=True)
```

### Step 10: Migrate database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 11: Create views to manage chat messages in chatbot_app/views.py
```python
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
```

### Step 12: Add Base HTML templates with Bootstrap CDN code at chatbot_app/templates/base.html you need to create the templates folder in the chatbot_app folder
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  
    <link rel="stylesheet" href="{% static 'css/styles.css' %}" />

    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
      crossorigin="anonymous"
    />
    <script
    src="https://unpkg.com/htmx.org@1.9.4"
    integrity="sha384-zUfuhFKKZCbHTY6aRR46gxiqszMk5tcHjsVFxnUo8VMus4kHGVdIYVbOYYNlKmHV"
    crossorigin="anonymous"
  ></script>

    <title>OpenAI Chat Clone</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="/index">OpenAI Chat Clone</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <a class="nav-link active" aria-current="page" href="/index">Home</a>
          </div>
        </div>
      </div>
    </nav>
    {% block content %} {% endblock %}
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
      crossorigin="anonymous"
      ></script>   
    <script>
        function clearInputField() {
    setTimeout(function() {
        document.getElementById('question-input').value = '';
    }, 100); // delay of 100 milliseconds
}
    </script>
  </body>
</html>
```

### Step 13: Create a chat.html file in chatbot_app/templates/chat.html
```html
        {% extends "base.html" %} {% block content %}
    <div class="container">
      <div id="conversation">
        <div class="mt-4 {% if forloop.last %}typewriter{% endif %}">
          <p class="p-2 rounded" style="background-color: #f0f0f0;">
           Hello! I am a chatbot. How can I help you today?
          </p>
        <div id="chatbox">
          {% include 'partials/_chat_box.html' %}
        </div>
        <div class="span htmx-indicator" id="loading">thinking ...</div>
        <form
          hx-post="{% url 'add_conversation' %}"
          hx-target="#chatbox"
          hx-indicator="#loading"
          id="chat-form"
          onsubmit="event.preventDefault(); clearInputField();"
        >
          {% csrf_token %}
          <div class="input-fields">
            <input class="form-control mb-4" type="text" name="message" id="question-input" />
            <button class="btn btn-primary" type="submit" >
              Send
            </button>
            <a href="{% url 'clear_chat' %}" class="btn btn-secondary">
              Clear Chat
            </a>
          </div>
        </form>
      </div>
    </div>
    {% endblock %}

```

### Step 14: Create a _chat_box.html file in chatbot_app/templates/partials/_chat_box.html
```html
{% if messages %}
<div>
  {% for message in messages %}
  <div class="mt-4">
    <p class="p-2 rounded" style="background-color: #007bff; color: #fff;">
      User: {{ message.user_message }}
    </p>
  </div>
  <div class="mt-4 {% if forloop.last %}typewriter{% endif %}">
    <p class="p-2 rounded" style="background-color: #f0f0f0;">
      Bot: {{ message.bot_message }}
    </p>
  </div>
  {% endfor %}
</div>
{% endif %}
```
## Step 15: Create a urls.py file in chatbot_app folder like -> chatbot_app/urls.py
```python
from django.urls import path
from .views import chat_view, clear_chat, add_conversation

urlpatterns = [
    path('', chat_view, name='chat_view'),
    path('clear_chat', clear_chat, name='clear_chat'),
    path('add_conversation', add_conversation, name='add_conversation'),
]
```

### Step 16: Add chatbot_app urls to chatbot_project/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chatbot_app.urls')),
]
```

### Step 17: Create chatbot_project/static/css/styles.css file folder and add a css file called 
```css
.typewriter p {
  overflow: hidden; /* Ensures the content is not revealed until the animation */
  border-right: 0.15em solid orange; /* The typwriter cursor */
  /* white-space: nowrap; Keeps the content on a single line */
  margin: 0 auto; /* Gives that scrolling effect as the typing happens */
  animation: typing 2.5s steps(40, end), blink-caret 0.75s step-end infinite;
}
/* The typing effect */
@keyframes typing {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}
/* The typewriter cursor effect */
@keyframes blink-caret {
  from,
  to {
    border-color: transparent;
  }
  50% {
    border-color: orange;
  }
}
```
### Step 18: Run the Django server
```bash
python manage.py runserver
```
finally

open url http://127.0.0.1:8000/chat/ in your browser

## Warning ##

This is a development server do not use in production !!!
