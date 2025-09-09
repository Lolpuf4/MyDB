from help_functions import*
from errors import*


def get_columns_CREATE_TABLE(command:str) -> tuple[list[str], str]:
    """

    :param command: command entered by the user
    :return: list of columns selected, name of the table
    """
    first_bracket = command.find("(")
    second_bracket = command.rfind(")")
    columns = command[first_bracket + 1: second_bracket]
    name_of_table = command[12: first_bracket].strip()
    items = columns.split(",")
    return items, name_of_table

def table_exists(table_name: str, database_name, username):
    file = get_database_structure(database_name, username)
    if table_name in file:
        return True
    else:
        return False

def column_exists(column, table_name, database_name, username):
    file = get_database_structure(database_name, username)
    if column in file[table_name]:
        return True
    else:
        return False

def generate_table(items:list, database_name, username) -> dict:
    """

    :param items:
    :return:
    """
    table = {"id": {"type": "integer", "unique": "True"}}
    for i in items:
        words = i.strip().split(" ")
        name_of_column = words[0].strip()
        data_type = words[1].strip()
        if name_of_column == "FOREIGN":
            refered_column = words[2].strip()[1 : -1]
            if not refered_column in table:
                raise UnknownColumnInForeignKeyError(refered_column)
            first_bracket1 = words[4].find("(")
            second_bracket2 = words[4].rfind(")")
            reference_column = words[4][first_bracket1 + 1 : second_bracket2]
            reference_table = words[4][: first_bracket1]
            if not table_exists(reference_table, database_name, username):
                raise UnknownReferenceTableError(reference_table)
            if not column_exists(reference_column, reference_table, database_name, username):
                raise UnknownReferenceColumnError(reference_column)

            table[refered_column]["FOREIGN KEY"] = [reference_column, reference_table]


        elif data_type.startswith("varchar"):
            first_bracket1 = data_type.find("(")
            second_bracket2 = data_type.rfind(")")
            max_length = data_type[first_bracket1 + 1: second_bracket2]
            data_type = data_type[: first_bracket1]
            table[name_of_column] = {"type": data_type, "MAX_LENGTH": max_length}
        else:
            table[name_of_column] = {"type": data_type}
    return table

