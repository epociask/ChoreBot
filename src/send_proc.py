from twilio.rest import Client
import settings 
import os 
import json 
import datetime
import random 

client = Client(settings.TWILIO_SID_TOKEN, settings.TWILIO_AUTH_TOKEN)
roommates: dict = settings.ROOMMATES
yesterdays_assignments: dict = None 
odd_week: bool = True 
chore_struct: dict = {}


with open("chores.json") as fr:
    chore_struct = json.load(fr)



print(chore_struct)

def run() -> None:
    hasUpdated: bool = False 
    while True:
        now = datetime.datetime.now()


        if now.minute == 8: #time to assign chores 
           assigned = generateChoreAssignments()
            


        if now.minute == 0 and(now.hour == 12 or now.hour == 20) and hasUpdated is False:
            hasUpdated = True 

        if now.minute != 0 and hasUpdated:
            hasUpdated = False 




def sendTextUpdates(assigned_chores: dict) -> None:
    global roommates
    chores_string = buildAssignmentString(assigned_chores)
    for name in roommates.keys():
        message = client.messages.create(
                                    body=f"Today's chore assignment is as follows: \n{chores_string}",
                                    from_=settings.TWILIO_NUMBER,
                                    to=roommates[name],
                                )



def getTodaysChores(dayOfWeek: int) -> list:
    global chore_struct
    chores_to_do: dict = []
    chores_to_do.append(chore_struct['daily'])
    del chore_struct['daily']
    for key in chore_struct.keys():
        for task_key in chore_struct[key].keys():
            if chore_struct[key][task_key] == dayOfWeek:
                chores_to_do.append(task_key)


    return chores_to_do


def getChoresFromFile() -> dict:
    with open("assigned_chores.json") as fr:

        try:
            return json.load(fr)

        except Exception:
            return None 


def writeChores(chores: dict) -> None:
    with open("assigned_chores.json", "w") as fr:
        json.dump(fr, chores)

def generateChoreAssignments() -> dict:
    assigned_chores: dict = {}
    names = [e for e in roommates.keys()]
    for name in names:
        assigned_chores[name] = []
    passed_down: list = []

    dayOfWeek: int = datetime.datetime.today().weekday()
    todays_chores: list = getTodaysChores(dayOfWeek)
    random.shuffle(todays_chores)
    yesterdays_assignments = getChoresFromFile()
    min_num = len(todays_chores) // len(names)

    while len(todays_chores) > 0:
        for chore in todays_chores:
            random.shuffle(names)
            for name in names:                    
                if yesterdays_assignments is None or chore not in yesterdays_assignments[name]:
                    if chore in todays_chores:
                        if len(assigned_chores[name]) < min_num:
                            assigned_chores[name].append(chore)
                            todays_chores.remove(chore)


        
    return assigned_chores



def buildAssignmentString(assigments: dict) -> str:

    def buildChoreString(name: str, chore_list: str) -> str:
        string_list = "\n-".join(item.title() for item in chore_list)
        return f"\n{name}: \n-{string_list}"
    
    return "\n".join(buildChoreString(name, chore_list) for name, chore_list in assigments.items())


