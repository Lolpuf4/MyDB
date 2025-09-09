from select import select

from errors import ColumnIsNotInTableError
from help_functions import get_database_structure


def split_column_name(column_name):
    if "." in column_name:
        column = column_name.split(".")[1]
    else:
        column = column_name
    return column

def get_data_with_conditions(data_base: dict, name_of_table: str, where: list[str], selected_columns: list[str]) -> list[list[str]]:
    """

    :param data_base: name of the database
    :param name_of_table: name of the table used
    :param where: list with the where statement
    :return: list with lists containing the record that follows the where conditions
    """
    data = []
    new_columns = []
    for column in selected_columns:
        new_columns.append(split_column_name(column))
    if not where is None:
        table_data = data_base[name_of_table]
        for record in table_data:
            if check_and(record, where):
                record = remove_extra_from_record(record, new_columns)
                data.append(record)
    else:
        table_data = data_base[name_of_table]
        for record in table_data:
            record = remove_extra_from_record(record, new_columns)
            data.append(record)

    return data

def get_longest_variables(select_columns: list[str], data:list[dict]) -> dict:
    """
    :param select_columns:  list of columns selected
    :param data: list of records
    :return: dict of columns with the longest values
    """
    longest_variables = {}
    new_columns = []
    for column in select_columns:
        new_columns.append(split_column_name(column))

    for i in new_columns:
        longest_variables[i] = len(i)
    for i in data:
        for record, column in zip(i, new_columns):
            if len(record[column]) > longest_variables[column]:
                longest_variables[column] = len(record[column])
    return longest_variables



def make_table(data: list[list[dict]], select_columns: list[str], table: str) -> str:
    """

    :param data: list of records
    :param select_columns: list of columns selected
    :param table: name of the table selected
    :return: the table with the selected columns
    """
    result_table = ""
    longest_variables = get_longest_variables(select_columns, data)
    new_columns = []
    for column in select_columns:
        new_columns.append(split_column_name(column))

    for column in new_columns:
        result_table += column + f"{(longest_variables[column] + 1 - len(column)) * ' '}| "
    result_table = result_table[:-2]
    result_table += f"\n{len(result_table) * "-"}\n"
    for i in data:
        for record, column in zip(i, new_columns):
            if not column in record:
                raise ColumnIsNotInTableError(column, table)
            else:
                result_table += record[column] + f"{((longest_variables[column] + 1) - len(record[column])) * ' '}| "
        result_table = result_table[:-3]
        result_table += "\n"
    return result_table


def get_where_and_selected_columns(command:str) -> tuple[str, list[str] | None, list[str]]:
    """

    :param command: the command entered by the user
    :return: name of the table that the user is trying to work with, the where statement as a list with strings inside or None and the selected columns by the user
    """
    select = command[6:].split("FROM")[0].strip()
    where = None
    if "WHERE" in command:
        name_of_table = command[6:].split("FROM")[1].split(" ")[1]
        where_temp = command.split("WHERE")[1].strip()
        where_and_temp = where_temp.split("AND")
        where_temp1 = []
        for i in where_and_temp:
            i = i.strip()
            where_temp1.append(i.split(" "))
        where = []
        for i in where_temp1:
            where.append([])
            for j in i:
                where[-1].append(j.strip())

    else:
        name_of_table = command[6:].split("FROM")[1].strip()[:-1]
    select_columns = select.split(", ")



    return name_of_table, where, select_columns


# def get_join_statement(command:str) -> tuple[list[str], str, str, str, str]:
#     """
#
#     :param command: the command entered by the user
#     :return: a tuple with: from table, join table, column1, column2 names
#     """
#     list = command[6:].split(" FROM ")[0].strip().split(", ")
#     from_table_name = command[6:].split(" FROM ")[1].split(" JOIN ")[0].strip()
#     join_table_name = command[6:].split(" FROM ")[1].split(" JOIN ")[1].split(" ON ")[0].strip()
#     temp_statement = command[6:].split(" FROM ")[1].split(" JOIN ")[1].split(" ON ")[1].strip()
#     column1 = temp_statement.split("=")[0].strip()
#     column2 = temp_statement.split("=")[1].strip().replace(";", "")
#     return list, from_table_name, join_table_name, column1, column2
#
# def inner_join(command:str, database:dict) -> tuple[list[dict[str]], list[str]]:
#     columns, from_table_name, join_table_name, column1, column2 = get_join_statement(command)
#     print(columns, from_table_name, join_table_name, column1, column2)
#     all_combined = []
#     for column in columns:
#         table_name = column.split(".")[0]
#         column_name = column.split(".")[1]
#         for record1 in database[from_table_name]:
#             for record2 in database[join_table_name]:
#                 if record1[column1.split(".")[1]] == record2[column2.split(".")[1]]:
#                     combined_record = {}
#
#                     if table_name == from_table_name:
#                         combined_record[column_name] = record1[column_name]
#                     else:
#                         print("record2", record2)
#                         combined_record[column_name] = record2[column_name]
#                 all_combined.append(combined_record)
#
#     return all_combined, columns

def get_join_statement(command:str) -> tuple[list[str], str, list[str], list[str], list]:
    """

    :param command: the command entered by the user
    :return: a tuple with: from table, join table, column1, column2 names
    """
    select_columns = command[6:].split(" FROM ")[0].strip().split(", ")
    from_table_name = command[6:].split(" FROM ")[1].split(" JOIN ")[0].strip()
    join_tables = []
    join_statements = []
    command_split_by_spaces = command.split(" ")
    for i in range(0, len(command.split(" "))):
        if command_split_by_spaces[i].strip() == "JOIN" :
            join_tables.append(command_split_by_spaces[i + 1].strip())
        if command_split_by_spaces[i].strip() == "ON":
            text = ""
            for word in command_split_by_spaces[i + 1: i+4]:
                text += word + " "
            join_statements.append(text.strip())
    name_of_table, where, select_columns = get_where_and_selected_columns(command)

    return select_columns, from_table_name, join_tables, join_statements, where


def inner_join(command:str, database:dict):
    select_columns, from_table_name, join_tables, join_statements, where = get_join_statement(command)
    if "*" in select_columns:
        select_columns.clear()
        all_tables = join_tables + [from_table_name]
        for table in all_tables:
            structure = get_database_structure("messenger", "admin")
            for column in structure[table]:
                select_columns.append(f"{table}.{column}")


    all_combined = []

    join_statement = [join_statements[0].split(" ")[0], join_statements[0].split(" ")[2]]
    first_table_updated = add_table_name_to_records(database[from_table_name], from_table_name)
    second_table_updated = add_table_name_to_records(database[join_tables[0]], join_tables[0])



    all_combined.extend(join_two_tables(from_table_name, join_tables[0], first_table_updated, second_table_updated, join_statement))
    for i in range(1, len(join_tables)):
        join_statement = [join_statements[i].split(" ")[0], join_statements[i].split(" ")[2]]
        table1 = join_statement[0].split(".")[0]
        table2 = join_statement[1].split(".")[0]
        if table1 != join_tables[i]:
            table_name1 = table1
        else:
            table_name1 = table2

        second_table_updated = add_table_name_to_records(database[join_tables[i]], join_tables[i])

        all_combined = join_two_tables(table_name1, join_tables[i], all_combined, second_table_updated, join_statement)
    temp_data = []
    if where is None:
        temp_data = all_combined
    data = []
    if where is not None:
        for record in all_combined:
            result = check_and(record, where)
            if result:
                temp_data.append(record)

    for record in temp_data:
        temp_dict = {}
        for column in record:
            if column in select_columns:
                temp_dict[column] = record[column]
        data.append(temp_dict)
    return data


#"SELECT users.username, messages.text FROM message_history JOIN users ON message_history.senderID = users.id JOIN messages ON message_history.msgID = messages.id;"

def join_two_tables(table_name1, table_name2, records1, records2, join_statement):
    before_equal_sign = join_statement[0]
    after_equal_sign = join_statement[1]
    table1 = before_equal_sign.split(".")[0]
    column1 = before_equal_sign.split(".")[1]
    table2 = after_equal_sign.split(".")[0]
    column2 = after_equal_sign.split(".")[1]
    tables_combined = []


    #print(before_equal_sign, "records1", records1)
    #print(after_equal_sign, "records2", records2)
    for record1 in records1:
        for record2 in records2:
            if table1 == table_name1:
                if record1[before_equal_sign] == record2[after_equal_sign]:
                    record_combined = combine_records(record1, record2)
                    tables_combined.append(record_combined)
            else:
                if record2[before_equal_sign] == record1[after_equal_sign]:
                    record_combined = combine_records(record2, record1)
                    tables_combined.append(record_combined)

    return tables_combined



#обдумать структуру и решить задачу



def combine_records(record1, record2):
    record_combined = {}
    for j in record2:
        record_combined[j] = record2[j]
    for i in record1:
        record_combined[i] = record1[i]
    return record_combined

def add_table_name_to_record(record, table_name):
    updated_record = {}
    for i in record:
        updated_record[f"{table_name}.{i}"] = record[i]
    return updated_record

def add_table_name_to_records(records, table_name):
    records_updated = []
    for record in records:
        records_updated.append(add_table_name_to_record(record, table_name))
    return records_updated

def check_and(record: dict, conditions: list[list[str]]) -> bool:
    """

    :param record: record checking for where statement
    :param conditions: where conditions
    :return: True if conditions is true and False if conditions is false
    """
    for condition in conditions:

        try:
            if condition[1] == "=" and not int(record[condition[0]]) == int(condition[2]):
                return False
            elif condition[1] == ">" and not int(record[condition[0]]) > int(condition[2]):
                return False
            elif condition[1] == "<" and not int(record[condition[0]]) < int(condition[2]):
                return False
            elif condition[1] == "!=" and not int(record[condition[0]]) != int(condition[2]):
                return False
        except ValueError:
            if condition[1] == "=" and not (record[condition[0]]) == (condition[2]):
                return False
            elif condition[1] == ">" and not (record[condition[0]]) > (condition[2]):
                return False
            elif condition[1] == "<" and not (record[condition[0]]) < (condition[2]):
                return False
            elif condition[1] == "!=" and not (record[condition[0]]) != (condition[2]):
                return False
    return True


def remove_extra_from_record(record, columns_to_keep):
    new_record = {}
    for column in record:
        if column in columns_to_keep:
            new_record[column] = record[column]
    return new_record