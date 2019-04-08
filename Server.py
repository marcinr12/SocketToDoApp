from socket import *

import pickle
import json


def save_to_json(database):
    data = {'Database': []}

    for i, x in enumerate(database):
        data['Database'].append({'Task' + str(i + 1): database[i]})

    with open('database.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


server = socket(AF_INET, SOCK_STREAM)  	# creating socket
server.bind(('localhost', 8888))  		# binding socket
server.listen(10)

tasks_database = []

bool = 1

number_of_tasks = -1

ID = 0

with open('database.json', 'w') as outfile:
    json.dump('', outfile)

while bool:

    client, address = server.accept()  # connection from
    print ('Connection from ', address)

    while 1:
        choice = client.recv(1024)
        if choice == "add_task":  # adding task to database
            task_pickle = client.recv(1024)
            task = pickle.loads(task_pickle)
            task.append(ID)
            ID += 1
            tasks_database.append(task)
            save_to_json(tasks_database)

        elif choice == "delete_task":
            index = client.recv(1024)
            for i, x in enumerate(tasks_database):
                if tasks_database[i][2] == int(index):
                    del tasks_database[int(index)]
            save_to_json(tasks_database)

        elif choice == "display_tasks":
            print (tasks_database)

            tasks_database_pickle = pickle.dumps(tasks_database)
            client.send(tasks_database_pickle)

        elif choice == "display_task_knowing_priority":
            priority = client.recv(1024)
            task_priority = []
            for i, x in enumerate(tasks_database):
                print (tasks_database[i][0])
                if tasks_database[i][0] == str(priority):
                    task_priority.append(tasks_database[i])
            print (task_priority)

            task_priority_pickle = pickle.dumps(task_priority)
            client.send(task_priority_pickle)

        elif choice == "shutdown_server":
            bool = 0
            break

    client.close()
