def writeToJSON(data_struct: dict, fileName="assigned_chores.json") -> None:
    with open(fileName, "w") as fr:
        json.dump(data_struct, fr)