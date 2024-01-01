#!/usr/bin/python3.7
import requests
from twilio.rest import Client
import json

# Twilio credentials
account_sid = "[[redacted]]"  # Replace with actual Account SID
auth_token = "[[redacted]]"    # Replace with actual Auth Token
client = Client(account_sid, auth_token)

# Target phone numbers
to_phone_number = "+18325104535"
from_phone_number = "+18447356172"

# API endpoint
url_lookup = "https://sentry.cordanths.com/Sentry/WebCheckin/Lookup"
url_log = "https://sentry.cordanths.com/Sentry/WebCheckin/Log"

# Headers and payload for the POST requests
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

# These are the variables that will be used when a signs up. Phone = Phone to IVR, last = Last Name, ivr_code = Unique pin assigned to user
payload = {
    "phone": "9362834848",
    "last_name": "Mayo",
    "ivr_code": "241430",
    "lang": "en"
}

# Function to send SMS via Twilio
def send_sms(body):
    message = client.messages.create(
        to=to_phone_number,
        from_=from_phone_number,
        body=body
    )
    print("Message Sent, SID:", message.sid)

# Send Request 01
try:
    response_01 = requests.post(url_lookup, headers=headers, data=payload)
    response_01.raise_for_status()  # Check if the request was successful
    
    # Extract image id from response
    response_data = json.loads(response_01.text)
    try:
        image_id = response_data[0]['img']
    except KeyError:
        print("Key 'img' not found in the response data:", response_data)
    
    # Check for API error messages
    if 'error_msg' in response_data[0]:
        error_msg = response_data[0]['error_msg']
        print("API Error:", error_msg)
        
        # Send SMS with error message
        send_sms(error_msg)
        
    else:
        # Send Request 03
        try:
            response_03 = requests.post(url_log, headers=headers, data=payload)
            response_03.raise_for_status()  # Check if the request was successful
            
            response_data = json.loads(response_03.text)
            try:
                text_message = response_data[0]['text']
                date_message = response_data[0]['date']
                transaction_key = response_data[0]['transaction_key']
            except KeyError as e:
                print(f"Key {str(e)} not found in the response data:", response_data)
            
            # Check the 'text' value and send SMS accordingly
            if text_message == "Do not test today":
                sms_body = str(response_data)
            else:
                sms_body = str(response_data)
            
            # Send SMS via Twilio
            send_sms(sms_body)
            
        except requests.RequestException as e:
            print("Request 03 failed:", str(e))
    
except requests.RequestException as e:
    print("Request 01 failed:", str(e))

