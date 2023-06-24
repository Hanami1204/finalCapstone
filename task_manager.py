# This is a task manager system
# User can register new users, assign tasks, generate and view reports
# Data are saved in external txt and are read every time the program starts
# Generated reports are saved in txt files as well
# SKILLS: data i/o

# =====importing libraries===========
import os
from datetime import datetime, date


def reg_user():
    """Add a new user to the system, then update the user.txt file"""
    global user_data
    new_username = input("New Username: ")
    if new_username in username_password:
        print('Error, username already exists')
        return
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    # check if the new password and confirmed password are the same
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        # add new user's information in 'user.txt'
        with open("user.txt", "a") as out_file:
            out_file.write(f'\n{new_username};{new_password}')
    else:  # password matches not
        print("Passwords do no match. Action unsuccessful, returning to main menu")


def add_task():
    """Allow a user to add a new task to 'task.txt'
        Prompt a user for the following:

        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and
        - the due date of the task."""

    # ask task assignee, task title, task description, task due date
    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        task_username = input("User does not exist. Please enter a valid username, "
                              "enter 'exit' to return to main menu: ")
        if task_username == 'exit':
            return False
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD, e.g. 2023-11-15): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()

    # append the new task to task_list
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)

    # append the new task to the file task.txt
    with open("tasks.txt", "a") as file:
        file.write(task_list_to_txt())
    print("Task successfully added.")


def display_task(task):
    disp_str = f"Task: \t {task['title']}\n"
    disp_str += f"Assigned to: \t {task['username']}\n"
    disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Description: \n {task['description']}\n"
    disp_str += f"Task completed: {task['completed']}"
    print(disp_str)


def view_mine():
    """Reads the task from task.txt file and prints to the console in the
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)"""
    task_no = '1'
    my_tasks = {}
    for task in task_list:
        # save my tasks in a dictionary, number being key, task details being value
        if task['username'] == curr_user:
            print(f'\nNo.{task_no}')
            display_task(task)
            my_tasks[task_no] = task
            task_no = str(int(task_no) + 1)
    # print(my_tasks)  # test code

    # ask if user wants to select a task
    cmd = ''
    while cmd not in my_tasks and cmd != '-1':
        cmd = input('Input the number to select a task, input "-1" to return to main menu:\n')

    if cmd == '-1':
        return
    else:  # task selected
        selected_task = cmd
        cmd = ''
        # ask user what to do with the task
        while cmd != 'c' and cmd != 'e' and cmd != '-1':
            cmd = input('Input "c" to mark the task as complete, input "e" to edit the task, input "-1" to exit:\n')

        # set a task as complete
        if cmd == 'c':
            my_tasks[selected_task]['completed'] = True
            print('Task set as completed!')
            # update task status in tasks.txt
            with open('tasks.txt', 'w') as file:
                file.write(task_list_to_txt())
        # edit task details: assignee, due date
        elif cmd == 'e':
            if my_tasks[selected_task]['completed']:
                print('Sorry, this task is completed and cannot be edited')
                return
            else:
                cmd = ''
                while cmd != 'a' and cmd != 'd' and cmd != '-1':
                    cmd = input('Input "a" to edit task assignee, input "d" to edit due date, input "-1" to exit:\n')
                # assign task to another user
                if cmd == 'a':
                    new_user = ''
                    while new_user not in username_password and new_user != '-1':
                        new_user = input('Who do you wish to assign it to? Input "-1" to exit\n')
                    if new_user == '-1':
                        return
                    else:
                        my_tasks[selected_task]['username'] = new_user
                        # update task status in tasks.txt
                        with open('tasks.txt', 'w') as file:
                            file.write(task_list_to_txt())
                        print('Assign to another user successfully')
                # edit the due date
                elif cmd == 'd':
                    while True:
                        try:
                            new_due_date = input("Due date of task (YYYY-MM-DD, e.g. 2023-11-15): ")
                            new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            break
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified")
                    my_tasks[selected_task]['due_date'] = new_due_date
                    # update task status in tasks.txt
                    with open('tasks.txt', 'w') as file:
                        file.write(task_list_to_txt())
                    print('due date change succeeded')
                elif cmd == '-1':
                    return
        # exit to main menu
        elif cmd == '-1':
            return


def view_all():
    for task in task_list:
        display_task(task)


def task_list_to_txt():
    """Save all data in task_list as a long string to be saved in txt file
    To update the txt file, use:
    # update task status in tasks.txt
    with open('tasks.txt', 'w') as file:
        file.write(task_list_to_txt())"""
    each_task = []
    for task in task_list:
        str_attrs = [
            task['username'],
            task['title'],
            task['description'],
            task['due_date'].strftime(DATETIME_STRING_FORMAT),
            task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
            "Yes" if task['completed'] else "No"
        ]
        each_task.append(";".join(str_attrs))
    task_list_txt = '\n'.join(each_task)
    return task_list_txt


def percentage(part, whole):
    """Input part and whole, return a number representing percentage rounded up to 2 decimals.
    Needs adding % when printing as a percentage"""
    decimal = 2
    return round(100 * float(part) / float(whole), decimal)


def generate_task_overview():
    """Write task overview to 'task_overview.txt'.
    Report includes:

    - Total number of tasks:\t{}\n
    - Total number of completed tasks:\t{}\n
    - Total number of uncompleted tasks:\t{}\n
    - The total number of overdue tasks:\t{}\n
    - The percentage of unfinished tasks:\t{}%\n
    - The percentage of overdue tasks:\t{}%\n"""
    completed_task_num = 0
    unfinished_task_num = 0
    overdue_task_num = 0
    total_task_num = len(task_list)
    for task in task_list:
        # count completed and unfinished tasks
        if task['completed']:
            completed_task_num += 1
        else:
            unfinished_task_num += 1
            # count overdue tasks
            if task['due_date'].date() < date.today():
                overdue_task_num += 1
    with open('task_overview.txt', 'w') as file:
        if total_task_num != 0:
            file.write(
                f'TASK OVERVIEW\n'
                f'Total number of tasks:\t{total_task_num}\n'
                f'Total number of completed tasks:\t{completed_task_num}\n'
                f'Total number of uncompleted tasks:\t{unfinished_task_num}\n'
                f'The total number of overdue tasks:\t{overdue_task_num}\n'
                f'The percentage of unfinished tasks:\t{percentage(unfinished_task_num, total_task_num)}% '
                f'(out of all tasks)\n'
                f'The percentage of overdue tasks:\t{percentage(overdue_task_num, unfinished_task_num)}% '
                f'(out of unfinished tasks)'
                f'\t{percentage(overdue_task_num, total_task_num)}% (out of all tasks)'
            )
        else:
            file.write('TASK OVERVIEW\nThere is currently no task now')
    print('report generated successfully!')


def generate_user_overview():
    """Write task overview to 'task_overview.txt'.
\nReport includes:

- The total number of users registered with task_manager.py.
- The total number of tasks that have been generated and tracked using task_manager.py.

and each user's:

- The total number of tasks assigned to that user.
- The percentage of the total number of tasks that have been assigned to that user
- The percentage of the tasks assigned to that user that have been completed
- The percentage of the tasks assigned to that user that must still be completed
- The percentage of the tasks assigned to that user that have not yet been completed and are overdue
    """
    user_num = len(username_password)
    total_task_num = len(task_list)
    user_task_track = {}
    """
    user_task_track, the structure:
    {'user1':{
         'assigned_task_num': n
         'assigned_task_percentage': n%
         'completed_task_percentage': n%
         'unfinished_tasks_percentage': n%
         'overdue_tasks_percentage': n%
     }
     'user2':{
          same pattern
     }
    }"""
    # save all user and their related tasks in dictionary
    for user in username_password:
        user_task_info = {}
        task_assigned = 0
        completed_task = 0
        overdue_task = 0
        for task in task_list:
            if task['username'] == user:
                # count assigned tasks for that user
                task_assigned += 1
                # count completed tasks for that user
                if task['completed']:
                    completed_task += 1
                # count overdue tasks
                else:  # all unfinished tasks
                    if task['due_date'].date() < date.today():
                        overdue_task += 1

        unfinished_task = task_assigned - completed_task
        user_task_info['assigned_task_num'] = task_assigned
        # skip calculating statistics for users without any assigned tasks
        if task_assigned != 0:
            user_task_info['assigned_task_percentage'] = percentage(part=task_assigned, whole=total_task_num)
            user_task_info['completed_task_percentage'] = percentage(part=completed_task, whole=task_assigned)
            user_task_info['unfinished_task_percentage'] = percentage(part=unfinished_task, whole=task_assigned)
            user_task_info['overdue_task_percentage'] = percentage(part=overdue_task, whole=task_assigned)
        # save data related to that user in a dictionary, username being the key
        user_task_track[user] = user_task_info

    with open('user_overview.txt', 'w') as file:
        file.write(f'USER OVERVIEW\n'
                   f'Total number of registered users: {user_num}\n'
                   f'Total number of recorded tasks: {total_task_num}\n')
        for user in username_password:
            # rule out users without any assigned tasks
            # print(user_task_track)  # test code
            if user_task_track[user]['assigned_task_num'] != 0:
                file.write(
                    f'\nUser: {user}\n'
                    f'The total number of tasks assigned to this user: {user_task_track[user]["assigned_task_num"]}\n'
                    f'The percentage of the total number of tasks that have been assigned to that user: '
                    f'{user_task_track[user]["assigned_task_percentage"]}%\n'
                    f'The percentage of the tasks assigned to that user that have been completed: '
                    f'{user_task_track[user]["completed_task_percentage"]}%\n'
                    f'The percentage of the tasks assigned to that user that must still be completed: '
                    f'{user_task_track[user]["unfinished_task_percentage"]}%\n'
                    f'The percentage of the tasks assigned to that user that are overdue: '
                    f'{user_task_track[user]["overdue_task_percentage"]}%\n'
                )
            else:
                file.write(f'\nUser: {user}\nThis user has not been assigned any tasks\n')
        # file.write(f'{user_task_track}')  # test code
        pass


# ++++++++++++++++++
# ====Initialise====
# ++++++++++++++++++

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# read all tasks from 'task.txt' and save in task_list
# task_list is to be a list containing dictionaries
# task_list is the main project management object
task_list = []
for t_str in task_data:
    curr_t = {}
    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    task_list.append(curr_t)

# +++++++++++++++++++++
# ====Login Section====
# +++++++++++++++++++++

'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data and convert to dictionary, username as key, password as value
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# read in username and password
logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# +++++++++++++++++++++++++
# ====operation section====
# +++++++++++++++++++++++++

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    if curr_user == 'admin':  # admin special command(s): gr
        menu = input('''
Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
s- statistics
gr - generate reports  
ds - Display statistics
e - Exit
: ''').lower()
    else:
        menu = input('''
Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
e - Exit
: ''').lower()

    # mode: register new user
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'vm':
        view_mine()
    elif menu == 'va':
        view_all()
    # If the user is an admin they can display statistics about number of users and tasks
    elif menu == 'ds' and curr_user == 'admin':
        num_users = len(username_password.keys())
        num_tasks = len(task_list)
        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")
    elif menu == 'ds' and curr_user != 'admin':
        print('Sorry, this function is for administrator only')
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    elif menu == 'gr' and curr_user == 'admin':
        generate_task_overview()
        generate_user_overview()
    # test mode
    # =========
    elif menu == 's' and curr_user == 'admin':
        generate_task_overview()
        generate_user_overview()
        with open('task_overview.txt', 'r') as file:
            content = file.read()
            print(f'\n{content}\n')
        with open('user_overview.txt', 'r') as file:
            content = file.read()
            print(f'\n{content}\n')
    elif menu == 'test':
        print(f'{username_password}')
    else:
        print("Sorry, unrecognised input, please Try again")
