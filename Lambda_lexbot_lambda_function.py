import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('lexbot1')

def lambda_handler(event, context):
    try:
        slots = event['sessionState']['intent']['slots']
        slot_values = {key: value['value']['interpretedValue'] for key, value in slots.items()}

        item = {'pestreportid': str(uuid.uuid4()), **slot_values}
        table.put_item(Item=item)

        response_message = "\n".join(f"{key}: {value}" for key, value in slot_values.items())
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": event['sessionState']['intent']['name'], "state": "Fulfilled"}
            },
            "messages": [{"contentType": "PlainText", "content": f"Thank you! Here is the information you provided:\n{response_message}"}]
        }
    
    except Exception:
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": "UnknownIntent", "state": "Failed"}
            },
            "messages": [{"contentType": "PlainText", "content": "Error processing your request."}]
        }
