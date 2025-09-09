from errors import ColumnIsNotInTableError


def get_ids(database: dict, name_of_table: str) -> list[int]:
    """

    :param database: the database file
    :param name_of_table: the name of the table selected
    :return:
    """
    ids = []
    for obj in database[name_of_table]:
        ids.append(int(obj["id"]))
    return ids

def get_column_info(database:dict, name_of_table:str, column:str) -> str:
    """

    :param database: the database file
    :param name_of_table: the name of the table selected
    :param column: the name of the column selected
    :return: the column's info from the database
    """
    columns = database[name_of_table]
    for column_info in columns:
        if column_info == column:
            return columns[column]
    raise ColumnIsNotInTableError(column, name_of_table)

def get_columns_and_values_and_name_of_table(command:str) -> tuple[list[str], list[str], str]:
    """
    :param command: the command entered by the user
    :return: list of columns the user has entered, the list of values the user has entered, the name of table
    """
    first_bracket = command.find("(")
    second_bracket = command.find(")")
    name_of_table = command[12: first_bracket].strip()
    columns = command[first_bracket +1  : second_bracket].split(", ")

    first_bracket = command.rfind("(")
    second_bracket = command.rfind(")")
    values = command[first_bracket + 1: second_bracket].split(", ")

    return columns, values, name_of_table

def creates_an_object_for_insert_into(data_base:dict, name_of_table:str, columns:list[str], values:list[str]) -> tuple[int, dict[str:str]]:
    """

    :param data_base: the database the user is working with
    :param name_of_table: name of the table
    :param columns: columns that are user
    :param values: values that are used
    :return: id of the object in the database, table made with the given values and columns
    """
    if len(data_base[name_of_table]) == 0:
        id_of_object = 1
    else:
        id_of_object = max(get_ids(data_base, name_of_table)) + 1
    print(id_of_object)

    table = {"id": str(id_of_object)}
    if len(columns) == len(values):
        for i in range(len(columns)):
            table[columns[i]] = values[i]
    return id_of_object, table


def saves_new_object_to_database_if_no_errors(structure_data, data_base, name_of_table, columns, values, id_of_object, table, save_database, database_name, username):
    if len(structure_data[name_of_table]) == len(columns) + 1:
        for i in range(len(columns)):
            if get_column_info(structure_data, name_of_table, columns[i])["type"] == "integer":
                for symbol in values[i]:
                    if not symbol in "1234567890":
                        raise ValueError("incorrect datatype")  # TODO change to own error

        data_base[name_of_table].append(table)
        save_database(data_base, database_name, username)

    else:
        raise ValueError("need more columns")