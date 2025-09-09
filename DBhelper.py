import socket
import threading
import json
from protocol import*
from errors import*
HOST = "127.0.0.1"
PORT = 10002

def execute_command(command, user, password, database = ""):
    socket_test_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_test_client.connect((HOST, PORT))
    if "/" in command and database == "":
        raise NoDatabaseError()
    try:
        send_text(socket_test_client, user)
        send_text(socket_test_client, password)
        send_text(socket_test_client, database)
        send_text(socket_test_client, command)

        information = recv(socket_test_client)
        if information[0] == "TXT":
            return information[1]
        elif information[0] == "ERR":
            raise DataBaseError(information[1])
        elif information[0] == "JSN":
            file = open(information[1], "r", encoding="UTF-8")
            file_info = json.load(file)
            file.close()
            return file_info
    except DataBaseError as e:
        print(e)
    finally:
        socket_test_client.close()



#print(execute_command("SELECT users.username, messages.text FROM users JOIN messages ON message_history.senderID = users.id", "admin", "123", "messenger"))


#print(execute_command("CREATE TABLE departments (department_name varchar(50));", "admin", "123", "messenger"))
#print(execute_command("CREATE TABLE employees (name varchar(100), department_id integer, FOREIGN KEY (department_id) REFERENCES departments(id));", "admin", "123", "messenger"))

#print(execute_command("SELECT employees.name, departments.department_name FROM employees JOIN departments ON employees.department_id = departments.id;", "admin", "123", "messenger"))




print(execute_command("SELECT users.username, messages.text FROM message_history JOIN users ON message_history.senderID = users.id JOIN messages ON message_history.msgID = messages.id WHERE users.id < 2;", "admin", "123", "messenger"))
#print(execute_command("SELECT username FROM users WHERE username = ilia;", "admin", "123", "messenger"))
#print(execute_command("SELECT employees.id, employees.name, departments.department_name FROM employees JOIN departments ON employees.department_id = departments.id;", "admin", "123", "messenger"))




