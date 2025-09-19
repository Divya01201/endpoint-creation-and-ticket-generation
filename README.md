# endpoint-creation-and-ticket-generation
receives the payload via webhook and generate a ticket in the ticket tool , one can also moify the ticket generation part and implement another task  

1. In this code we are basically creating a weboook endpoint , that redirect the traffic to the webhook endpoint 

2. when the endpoint would receive the payload from messagecentral 

3. It would hit the ticketingtool api if , the ticketing tool api would get all filed ,  successfull authentication the tool endpoint would generate a ticket , we can change the veriabel to be diaplay in the generated ticket 

4. Run this code with :**uvicorn main:app --reload --host 127.0.0.1 --port 8000**
It would create the localhost/webhook url "**http://127.0.0.1:8000**" 

5. Then open the postman - use the following 
url = http://localhost:8000/webhook
body = {
  "entry": [
    {
      "changes": [
        {
          "value": {
            "metadata": {"display_phone_number": "91966xxxxxx"},
            "contacts": [{"profile": {"name": "Divya"}, "wa_id": "111xxxxxx"}],
            "messages": [{"text": {"body": "Hello from WhatsApp"}}]
          }
        }
      ]
    }
  ]
}

Authoriztion = basic auth  - **key**
                              **X** 

     SEND
we would get 200 response 
"**ticket generated 201**"

6. now open the console 
you can see the payload received - valued that we entered in the body of postman
tool response 201 {{----------------}}
https OK

this means the ticket has been successfully generated 
