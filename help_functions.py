import json

def get_database(database, user) -> dict:
    """

    :return: loaded database file
    """
    file = open(f"databases/{user}_{database}.json", "r", encoding="UTF-8")
    data_base = json.load(file)
    file.close()
    return data_base
def get_database_structure(database, user) -> dict:
    """

    :return: loaded structure database file
    """
    file = open(f"databases/{user}_{database}_structure.json", "r", encoding="UTF-8")
    structure_data = json.load(file)
    file.close()
    return structure_data

def checkForCorrectPerentheses(text):
    parentheses_only_text = ""
    for i in text:
        if i == "(" or i == ")":
            parentheses_only_text += i


    open_parenthesis = []
    for parenthsesis in parentheses_only_text:
        if parenthsesis == '(':
            open_parenthesis.append(parenthsesis)
        elif parenthsesis == ')':
            if len(open_parenthesis) == 0:
                return False
            open_parenthesis.pop(0)
    if len(open_parenthesis) == 0:
        return True
    else:
        return False




print(checkForCorrectPerentheses(""))