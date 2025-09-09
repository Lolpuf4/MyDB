from create_table_functions import*
from insert_into_functions import*
from select_functions import*
from DBMS_functions import*





def remove_extra_spaces(command_temp:str) -> str:
    """

    :param command_temp: the command entered by the user
    :return: command with removed extra spaces
    """
    command = ""
    command_temp = " " + command_temp
    for i in range(1, len(command_temp)):
        if  command_temp[i] == " " and command_temp[i - 1] != " " or command_temp[i] != " ":
            if command_temp[i] == "\n":
                command += " "
            else:
                command += command_temp[i]
    print(command)
    return command


def save_database_structure(structure_data: dict, database_name, name):
    """

    :param structure_data: the structure database file
    :return: updates the database file
    """
    file = open(f"databases/{name}_{database_name}_structure.json", "w", encoding="UTF-8")
    json.dump(structure_data, file, ensure_ascii=False, indent=4)
    file.close()
def save_database(data_base: dict, database_name, name):
    """

    :param data_base: the database file
    :return: updates the database file
    """
    file = open(f"databases/{name}_{database_name}.json", "w", encoding="UTF-8")
    json.dump(data_base, file, ensure_ascii=False, indent=4)
    file.close()




def program_command(username, password, command):
    """

    :param command: the command entered by the user
    :return: result from the users command
    """

    command = remove_extra_spaces(command)

    if command[:15] == "/createDatabase":
        db_name = create_database(command, username)
        return f"Database {db_name} Created"
    else:
        raise UnknownCommandError(command)

def sql_command(username, password, database_name, command):
    if not checkForCorrectPerentheses(command):
        raise InvalidParenthesesError()

    data_base = get_database(database_name, username)
    structure_data = get_database_structure(database_name, username)
    command = remove_extra_spaces(command)



    if command[:12] == "CREATE TABLE":
        items, name_of_table = get_columns_CREATE_TABLE(command)
        table = generate_table(items, database_name, username)
        structure_data[name_of_table] = table
        save_database_structure(structure_data, database_name, username)
        data_base = get_database(database_name, username)
        data_base[name_of_table] = []
        save_database(data_base, database_name, username)
        return "Table Created"


    elif command[:11] == "INSERT INTO":
        columns, values, name_of_table = get_columns_and_values_and_name_of_table(command)
        id_of_object, table = creates_an_object_for_insert_into(data_base, name_of_table, columns, values)
        saves_new_object_to_database_if_no_errors(structure_data, data_base, name_of_table, columns, values, id_of_object, table, save_database, database_name, username)
        return str(id_of_object)


    elif command[:6] == "SELECT":
        if command[-1] == ";":
            command = command[:-1]
        if " JOIN " in command:
            data = inner_join(command, data_base)
        else:
            name_of_table, where, select_columns = get_where_and_selected_columns(command)
            print(name_of_table, "|||", where, "|||", select_columns)
            structure_data = get_database_structure(database_name, username)
            for column in select_columns:
                if not column in structure_data[name_of_table]:
                    raise ColumnIsNotInTableError(column, name_of_table)

            data = get_data_with_conditions(data_base, name_of_table, where, select_columns)
        file = open("temp.json", "w", encoding = "UTF-8")
        json.dump(data, file)
        file.close()
        return "temp.json"


        # (make_table(data, select_columns, name_of_table))

    # add OR in select where
    # order by in SELECT
    #check for more errors
    # check for errors that misuse of WHERE might cause


#print(program_command("ilia", "123", "/createDatabase test153252;"))


#create DB, connect DB
#log in account

