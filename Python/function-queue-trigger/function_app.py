import azure.functions as func
import logging
import smtplib

app = func.FunctionApp()

@app.queue_trigger(arg_name="azqueue", queue_name="emails-to-send",
                               connection="AZURE_STORAGE_CONNECTION_STRING") 
def queue_trigger(azqueue: func.QueueMessage):
    message_detail = azqueue.get_json()

    sender_email = message_detail['sender_email']
    receiver_email = message_detail['receiver_email']
    email_text = message_detail['email_text']

    logging.info(f"Sending email ✉️ from {sender_email} to {receiver_email} with text ✏️{email_text}")
    
  
