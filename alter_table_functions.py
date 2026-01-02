from .help_functions import*
from .errors import*

def add(command, username, database_name):
    # ALTER TABLE users ADD is_active BOOLEAN DEFAULT TRUE;
    table_name = command.split(" ")[2]
    field = command.split(" ")[4]
    new_value_type = command.split(" ")[5]
    new_value = command.split(" DEFAULT ")[1].split(" ")[0]


    database = get_database(database_name, username)
    database_structure = get_database_structure(database_name, username)

    table = database_structure[table_name]


    if new_value_type.startswith("VARCHAR"):
        first_bracket1 = new_value_type.find("(")
        second_bracket2 = new_value_type.rfind(")")
        max_length = new_value_type[first_bracket1 + 1: second_bracket2]
        new_value_type = new_value_type[: first_bracket1]
        table[field] = {"type": new_value_type, "MAX_LENGTH": max_length}
    else:
        table[field] = {"type": new_value_type}


    table[field]["unique"] = "True" if "UNIQUE" in command else "False"

    save_database_structure(database_structure, database_name, username)

    table = database[table_name]
    for record in table:
        record[field] = new_value

    save_database(database, database_name, username)
