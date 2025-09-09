from help_functions import*
def create_database(command, user):
    db_name = command.split(" ")[1][:-1]
    file = open("data.json", "r", encoding = "UTF-8")
    main_data = json.load(file)
    file.close()
    if db_name in main_data[user]["databases"]:
        raise ValueError("database with this name already exists")
    main_data[user]["databases"].append(db_name)

    file = open(f"data.json", "w", encoding="UTF-8")
    json.dump(main_data, file)
    file.close()

    file = open(f"databases/{user}_{db_name}.json", "w", encoding = "UTF-8")
    json.dump({}, file)
    file.close()
    file = open(f"databases/{user}_{db_name}_structure.json", "w", encoding="UTF-8")
    json.dump({}, file)
    file.close()
    return db_name