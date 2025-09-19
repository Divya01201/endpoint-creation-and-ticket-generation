from fastapi import FastAPI, Request
import requests
from requests.auth import HTTPBasicAuth

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "FastAPI server is running"}

# Freshdesk credentials
api_key = "4KgbOs39rbHGDLdqPLc"
# freshdesk_url = f"https://u2opiamobilepvtltd.freshdesk.com/api/v2/tickets"


@app.post("/feshDesk-webhook")
async def whatsapp_webhook(request: Request):
    try:
        payload = await request.json()
        print("Incoming Payload:", payload)

        # the required details parsed
        entry = payload.get("entry", [])[0]
        change = entry.get("changes", [])[0]
        value = change.get("value", {})

        display_number = value.get("metadata", {}).get("display_phone_number")
        contacts = value.get("contacts", [{}])[0]
        user_name = contacts.get("profile", {}).get("name")
        wa_id = contacts.get("wa_id")

        messages = value.get("messages", [])
        message_text = None
        if messages:
            message_text = messages[0].get("text", {}).get("body", "")

        # if message exists than only the ticket would generate 
        if display_number and user_name and wa_id and message_text:
            subject = f"WhatsApp Message from {user_name} ({wa_id})"
            description = (
                f"Display Number: {display_number}\n"
                f"  Name: {user_name}\n"
                f"  WA_ID: {wa_id}\n"
                f"  Message: {message_text}"
            )

            ticket_data = {
                "subject": subject,
                "description": description,
                "email": "divya.s@u2opiamobile.com",  # requester email
                "priority": 2,
                "status": 2,
                "source": 7,
            }

            response = requests.post(
                "https://u2opiamobilepvtltd.freshdesk.com/api/v2/tickets",
                json=ticket_data,
                auth=HTTPBasicAuth(api_key, "X")
            )

            print("Freshdesk Response:", response.status_code, response.text)
            return {"status": "ticket created", "freshdesk_status": response.status_code}

        return {"status": "missing fields, no ticket created"}

    except Exception as ex:
        print("Error:", str(ex))
        return {"status": "error", "details": str(ex)}
