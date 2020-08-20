from twilio.rest import Client
import settings 
import os 
import json 
import datetime
import utils
import random 

client = Client(settings.TWILIO_SID_TOKEN, settings.TWILIO_AUTH_TOKEN)
roommates: dict = settings.ROOMMATES
yesterdays_assignments = completed =  chore_struct = assigned = {}
odd_week: bool = True 

#TODO add local file caching for previous assignments to ensure no person is given same chore twice 
chore_struct = utils.readStructFromJSON("chores.json")


def run() -> None:
    hasUpdated = notCompleted = False 
    violationSent = True
    notCompleted = True
    isViolationTime = lambda time: time == 0 or time % 15 == 0 or time % 30 == 0 or time % 45 == 0

    while True:
        now = datetime.datetime.now()


        if now.hour == 8 and now.minute == 0 and hasUpdated is False: #time to build & assign today's chores 
            hasUpdated, notCompleted = True, True 
            global assigned
            assigned = generateChoreAssignments()
            hasUpdated = False 

        if not isViolationTime(now.minute):
            violationSent = False 

        if notCompleted is True and isViolationTime(now.minute) and violationSent is False:
            lazies = getLazyRoommates()
            violationSent = True 

            if len(lazies) == 0:
                notCompleted = False 

            else:
                punish(lazies)





def getLazyRoommates() -> list:
    completes: dict = utils.readStructFromJSON("completed.json")
    lazy_roommates: list = []
    times: int = 5 

    while (times:= times - 1) != 0: #Spams roommates five times 
        for key in completes.keys():
            if completes[key][0] is False:
                lazy_roommates.append(getNameForChore(key))


    return lazy_roommates


def punish(lazy_roomates: list) -> None:

    for name in lazy_roomates:
        client.messages.create(
                            body=f"DO YOUR CHORES {name}" + "!"*13,
                            from_=settings.TWILIO_NUMBER,
                            to=roommates[name],
                        )

def getNameForChore(chore: str):
    assigned: dict = utils.readStructFromJSON("assigned_chores.json")
    for name in assigned.keys():
        if chore in assigned[name]:
            return name 





def sendAssignedChoresSMS(assigned_chores: dict) -> None:
    global roommates
    global completed
    chores_string = utils.buildAssignmentString(assigned_chores, completed)
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
    for key in chore_struct.keys():
        if key != 'daily':
            for task_key in chore_struct[key].keys():
                if chore_struct[key][task_key] == dayOfWeek:
                    chores_to_do.append(task_key)


    return chores_to_do


def assignUID(vals: list) -> int:
    x: int = random.randint(1, 100)
    return x if x not in vals else assignUID(vals)

def buildCompletedStruct(todays_chores: dict) -> dict: 
    return {chore:[False, assignUID([]), []] for chore in todays_chores}

def generateChoreAssignments() -> dict:
    global completed
    global roommates
    todays_chores: list = getTodaysChores(datetime.datetime.today().weekday())
    names: list = [e for e in roommates.keys()]

    min_num: int = len(todays_chores) // len(names)
    remainder: int = len(todays_chores) % len(names)

    assigned_chores: dict = {name: [] for name in names}

    completed = buildCompletedStruct(todays_chores)

    utils.writeToJSON(completed, fileName="completed.json")
    random.shuffle(todays_chores)
    yesterdays_assignments = utils.readStructFromJSON("assigned_chores.json")

    while len(todays_chores) > 0:  #assignment algo hehehe
        for chore in todays_chores:
            random.shuffle(names)
            for name in names:                    
                if yesterdays_assignments is None or chore not in yesterdays_assignments[name]:
                    if chore in todays_chores:
                        if len(assigned_chores[name]) < min_num:
                            assigned_chores[name].append(chore)
                            todays_chores.remove(chore)


                        elif len(todays_chores) <= remainder + 1:
                            if random.randint(0,3) != 1:
                                continue

                            else:
                                assigned_chores[name].append(chore)
                                todays_chores.remove(chore)

    utils.writeToJSON(completed, fileName="completed.json")
    utils.writeToJSON(assigned_chores)
    return assigned_chores


todays = generateChoreAssignments()
sendAssignedChoresSMS(todays)

run()