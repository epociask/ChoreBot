from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import settings 
import json 
import utils

app = Flask(__name__)
 


assigned: dict = utils.readStructFromJSON("assigned_chores.json")
completed: dict = utils.readStructFromJSON("completed.json")

@app.route('/', methods=['POST'])
def handleText():
    incoming_msg = request.values.get('Body', '').lower().strip()
    resp = MessagingResponse()
    from_number = request.form['From']
    msg = resp.message()
    msg.body(deceipherMessage(incoming_msg, from_number))
    return str(resp)

def findName(phone_number: str) -> str:
    for name in settings.ROOMMATES.keys():
        if settings.ROOMMATES[name] == phone_number:
            return name 

    return None 

def updateStructs(chore: str, name: str) -> str:
    global completed
    global assigned
    names_updated_list: list = completed[chore][2]

    if name in names_updated_list:
        return "Sorry, it appears that you've already said that chore is completed"

    if chore in assigned[name]:
        return "Sorry, it appears that you are trying to validate your own chore ;)"    


    names_updated_list.append(name)
    
    if len(names_updated_list) == len(settings.ROOMMATES)-1:
        completed[chore][0] = True 
        utils.writeToJSON(completed, fileName="completed.json")

    return None

def deceipherMessage(message: str, phone_number: str) -> str: 
    global completed
    global assigned
    msg_list: list  = message.split(" ")
    name, chore_id = msg_list[0], msg_list[-1]

    try:
        chore_id = int(chore_id)

    except Exception:
        return "Chore ID is either not supplied or invalid"
        
    if name not in settings.ROOMMATES.keys():
        supported = ", ".join(e for e in settings.ROOMMATES.keys())
        return f"Invalid roommate name supplied... supported names are {supported}"

    for key, val in completed.items(): #basic verif
        if val[1] == int(chore_id):
            if key in assigned[name]:
                print("name", name)
                if (err := updateStructs(key, findName(phone_number))) !=  None:
                    return err

                else:
                    return utils.buildAssignmentString(assigned, completed)


            else:
                return "Name supplied does not correlate with given chore ID"



    return "chore ID supplied does not exist"



    

if __name__ == "__main__":
	app.run()
