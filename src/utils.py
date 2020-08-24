import json

def writeToJSON(data_struct: dict, fileName="assigned_chores.json") -> None:
    with open(fileName, "w") as fr:
        json.dump(data_struct, fr)


def readStructFromJSON(fileName: str) -> dict :
    with open(fileName, "r") as fr:
        return json.load(fr)


def buildAssignmentString(assigments: dict, completed: dict) -> str:

    def getCompletedEmoji(isDone: bool) -> str:
        return "✅" if isDone else "☐"
    
    def buildChoreString(name: str, chore_list: str) -> str:
        string_list = "\n-".join(f"{completed[item][1]}-- {item.title()} -> {getCompletedEmoji(completed[item][0])}" for item in chore_list) 
        return f"\n{name}: \n-{string_list}"

    return "\n".join(buildChoreString(name, chore_list) for name, chore_list in assigments.items())
