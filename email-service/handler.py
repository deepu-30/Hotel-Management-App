import json

def send_email(event, context):
    body = json.loads(event['body'])

    email_type = body.get("type")
    to_email = body.get("to")

    # For demo → no real email, just print
    print("Sending Email")
    print("Type:", email_type)
    print("To:", to_email)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Email simulated successfully"
        })
    }