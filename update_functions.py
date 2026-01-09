from .help_functions import*
from .errors import*

#UPDATE tablename SET isRead = 1;
def update(command, database_name, user):
    table_name = command.split(" ")[1]
    changes = command.split(" SET ")[1].split(" WHERE ")[0].split(", ")
    where_statement = command.split(" WHERE ")[1]
    where_column = where_statement.split(" = ")[0]
    where_value = where_statement.split(" = ")[1]
    database = get_database(database_name, user)
    for record in database[table_name]:
        for i in changes:
            column = i.split(" = ")[0]
            new_value = i.split(" = ")[1]
            if record[where_column] == where_value:
                record[column] = new_value
    save_database(database, database_name, user)