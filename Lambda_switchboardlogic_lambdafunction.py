def lambda_handler(event, context):
    try:
        intent_name = event['sessionState']['intent']['name']
        transfer_target = {
            "ReportPest": "PestReporting",
            "RequestControl": "PestControlAssistance",
            "Emergency": "HumanAgent"
        }.get(intent_name, "HumanAgent")

        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": intent_name, "state": "Fulfilled"},
                "sessionAttributes": {"transferTarget": transfer_target}
            }
        }
    
    except Exception:
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": "UnknownIntent", "state": "Failed"},
                "sessionAttributes": {"transferTarget": "HumanAgent"}
            },
            "messages": [{"contentType": "PlainText", "content": "Error processing your request."}]
        }
