from flask import Flask, request
import requests
import settings 
import send_proc
from twilio.twiml.messaging_response import MessagingResponse
import json 

app = Flask(__name__)
 

def readToStructJSON(fileName: str) -> dict:

    with open(fileName, "r") as fr:
        return json.load(fr)

assigned: dict = readToStructJSON("assigned_chores.json")
completed: dict = readToStructJSON("completed.json")

@app.route('/', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    msg.body()
    return str(resp)



def updateStructs(chore: str, name: str) -> str:
    global completed
    names_updated_list: list = completed[chore][3]

    if name in names_updated_list:
        return "Sorry, it appears that you've done an update"


    names_updated_list.append(name)
    
    if len(names_updated_list == len(settings.ROOMMATES)-1):
        completed[chore][0] = True 

    return None


    


    



def deceipherMessage(message: str) -> str: 
    global completed
    global assigned
    msg_list: list  = message.split(" ")
    name, chore_id = msg_list[0], msg_list[-1]

    if name not in settings.ROOMMATES.keys():
        supported = " ".join(e for e in settings.ROOMMATES.keys())
        return f"Invalid roommate name supplied... supported names are {supported}"

    for key, val in completed: #basic verif
        #TODO verify that name claiming chore completion isn't assigned to that ID
        if val[1] == chore_id:
            if key in assigned[name]:
               if (y := updateStructs(key, name)) !=  None:
                   return y 

                else:
                    return send_proc.buildAssignmentString(assigned)


            else:
                return "Name supplied does not correlate with given chore ID"



    return "chore ID supplied does not exist"



    

if __name__ == "__main__":
	app.run(debug=True)
