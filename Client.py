import pickle

from socket import *

server = socket(AF_INET, SOCK_STREAM)   # creating socket
server.connect(('localhost', 8888))     # connecting

choice = ""
while 1:
    print ("1. New task")
    print ("2. Display tasks")
    print ("3. Delete tasks")
    print ("4. Display tasks with knowing priority")
    print ("9. Shutdown server")
    print ("0. Shutdown client")
    choice = input()
    if choice == 1:          # creating net task
        print ("Creating new task...")
        priority = raw_input("Priority: ")
        name = raw_input("Name: ")
        task = [priority, name]
        task_pickle = pickle.dumps(task)
        server.send("add_task")
        server.send(task_pickle)
    elif choice == 2:
        print ("Tasks:")
        server.send("display_tasks")
        received_tasks_pickle = server.recv(1024)

        tasks = pickle.loads(received_tasks_pickle)
        print (tasks)

    elif choice == 3:

        task_id = raw_input("Enter ID of task to remove: ")
        server.send("delete_task")
        server.send(task_id)

    elif choice == 4:

        task_priority = raw_input("Enter priority o tasks to display: ")
        server.send("display_task_knowing_priority")
        server.send(task_priority)

        tasks_priority_pickle = server.recv(1024)
        tasks_priority = pickle.loads(tasks_priority_pickle)
        print (tasks_priority)

    elif choice == 9:
        print ("Shutting down...")
        server.send("shutdown_server")
    elif choice == 0:
        break
    else:
        print ("No such option.")


server.close()
