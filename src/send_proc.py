from twilio.rest import Client
import settings 
import os 
import datetime

client = Client(settings.TWILIO_SID_TOKEN, settings.TWILIO_AUTH_TOKEN)
roommates = settings.ROOMMATES


def run() -> None:

    while True:
        now = datetime.datetime.now()


        if now.minute == 8: #time to assign chores 
            #call assign chores function 


        if now.minute == 0 and(now.hour == 12 or now.hour == 20) and hasUpdated is False:
            hasUpdated = True 

        if now.minute != 0 and hasUpdated:
            hasUpdated = False 




def sendTextUpdates(assigned_chores: str) -> None:
    global roommates
    for name in roommates.keys():
        message = client.messages.create(
                                    body=name,
                                    from_=settings.TWILIO_NUMBER,
                                    to=roommates[name],
                                )



# sendUpdates()