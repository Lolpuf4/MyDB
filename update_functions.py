from .help_functions import*
from .errors import*

#UPDATE tablename SET isRead = 1;
def update(command, database_name, user):
    table_name = command.split(" ")[1]
    changes = command.split(" SET ")[1].split(", ")
    database = get_database(database_name, user)
    for record in database[table_name]:
        for i in changes:
            column = i.split(" = ")[0]
            new_value = i.split(" = ")[1]
            record[column] = new_value
    save_database(database, database_name, user)