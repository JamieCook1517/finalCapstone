# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


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


#====Function Definitions===
    
def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = input("New Username: ")

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Checking for duplicate usernames (while username is already in username_password dict)
    while new_username in username_password.keys():
        print("Username already exists. Try a different username.")
        new_username = input("New Username: ")
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        # - If they are the same, add them to the user.txt file,
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do not match")

def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        else:
            break
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")    

def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t\t {t['title']}\n"
        disp_str += f"Assigned to: \t\t {t['username']}\n"
        disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \t {t['description']}\n"
        disp_str += f"Completed: \t\t {'Yes' if t['completed'] else 'No'}\n"
        print(disp_str)

def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
        '''
    while True:
        task_choice = None

        # - Creating list of current user's tasks
        curr_user_task_list = list(filter(lambda t: t['username'] == curr_user, task_list))
        for i, t in enumerate(curr_user_task_list, 1):
            disp_str = f"\n{i}\n"
            disp_str += f"Task: \t\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            disp_str += f"Completed: \t\t {'Yes' if t['completed'] else 'No'}"
            print(disp_str)

        while True:
            try:
                if len(curr_user_task_list) > 0:
                    task_choice = int(input('''
Select the task you would like to edit (type number corresponding to your chosen task)
Type -1 to return to the main menu                                
'''))
                else:  # If empty
                    task_choice = int(input("\nYou do not have any tasks. Type -1 to return to the main menu. "))
                
                task_action = None
                action_done = False
                
                if 1 <= task_choice <= len(curr_user_task_list): # If valid number
                    index = task_choice - 1
                    disp_str = f"\n{task_choice}\n"  # Displaying chosen task
                    disp_str += f"Task: \t\t\t {curr_user_task_list[index]['title']}\n"
                    disp_str += f"Assigned to: \t\t {curr_user_task_list[index]['username']}\n"
                    disp_str += f"Date Assigned: \t\t {curr_user_task_list[index]['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Due Date: \t\t {curr_user_task_list[index]['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Task Description: \t {curr_user_task_list[index]['description']}\n"
                    disp_str += f"Completed: \t\t {'Yes' if curr_user_task_list[index]['completed'] else 'No'}"
                    print(disp_str)
                    print()
                    print('This is the task you are viewing.\n')

                    while True:
                        task_action = input('''Type 'mark' to mark as complete
Type 'edit' to edit task (only incomplete tasks can be edited)
Type 'back' to go back
''')
                        if task_action == 'back':
                            break

                        # - Marking task as complete
                        elif task_action.lower().strip() == 'mark':
                            if curr_user_task_list[index]['completed']:
                                print("Task is already completed. You should go back.\n")
                            else:
                                curr_user_task_list[index]['completed'] = 'Yes'
                                with open('tasks.txt', 'w') as file:  # Rewriting data to tasks.txt
                                    for t in task_list:
                                        values_string = ';'.join(list(t.values())[:3])
                                        file.write(values_string)
                                        file.write(f";{t['due_date'].strftime(DATETIME_STRING_FORMAT)}")
                                        file.write(f";{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
                                        file.write(f";{'Yes' if t['completed'] else 'No'}\n")
                                action_done = True
                                input("Task successfully marked as complete. Press ENTER to continue.")
                                break
                        
                        # - Editing task
                        elif task_action.lower().strip() == 'edit':
                            if curr_user_task_list[index]['completed']:
                                print("You cannot edit a complete task. You should go back.\n")
                            else:
                                edit_choice = input("Select one of the options to edit (user, due date): ")

                                # -- Editing user
                                if edit_choice == 'user':
                                    while True:
                                        user_choice = input("Type in username of person to assign task to: ")
                                        if user_choice not in username_password.keys():
                                            print("User does not exist. Please enter a valid username")
                                        else:
                                            break
                                    curr_user_task_list[index]['username'] = user_choice
                                    with open('tasks.txt', 'w') as file:
                                        for t in task_list:
                                            values_string = ';'.join(list(t.values())[:3])
                                            file.write(values_string)
                                            file.write(f";{t['due_date'].strftime(DATETIME_STRING_FORMAT)}")
                                            file.write(f";{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
                                            file.write(f";{'Yes' if t['completed'] else 'No'}\n")
                                    action_done = True
                                    input("Task successfully reassigned. Press ENTER to continue.")
                                    break

                                # -- Editing due date
                                elif edit_choice == 'due date':
                                    while True:
                                        try:
                                            date_choice = input("Type in new due date of task (YYYY-MM-DD): ")
                                            new_date_time = datetime.strptime(date_choice, DATETIME_STRING_FORMAT)
                                            break
                                        except ValueError:
                                            print("Invalid datetime format. Please use the format specified")
                                    curr_user_task_list[index]['due_date'] = new_date_time
                                    with open('tasks.txt', 'w') as file:
                                        for t in task_list:
                                            values_string = ';'.join(list(t.values())[:3])
                                            file.write(values_string)
                                            file.write(f";{t['due_date'].strftime(DATETIME_STRING_FORMAT)}")
                                            file.write(f";{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
                                            file.write(f";{'Yes' if t['completed'] else 'No'}\n")
                                    action_done = True
                                    input("Successfully edited due date. Press ENTER to continue.")
                                    break

                                else:
                                    print("Invalid option.\n")
                        else:
                            print("Invalid option.\n")

                if task_choice == -1 or task_action == 'back' or action_done:
                    break
                else:
                    print("Invalid number.") if len(curr_user_task_list) > 0 else print("Please type in -1.")
            except ValueError:
                print(f"""Please type in {"a number." if len(curr_user_task_list) > 0 else "-1."}""")

        if task_choice == -1:  # Once task_choice is -1 from inner while loop
            break

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

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


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()
            
    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        '''Generates reports written to task_overview.txt and user_overview.txt'''

        curr_date = date.today().strftime(DATETIME_STRING_FORMAT)
        num_curr_date = int(''.join(curr_date.split('-')))  # Removing hyphens

        # Naming Variables for task_overview.txt      
        num_tasks = len(task_list)
        completed = len([t for t in task_list if t['completed']])
        uncompleted = len([t for t in task_list if not t['completed']])
        overdue = len([t for t in task_list if num_curr_date >= int(
            ''.join(t['due_date'].strftime(DATETIME_STRING_FORMAT).split('-'))  # e.g. 20240217 >= 20240212 (overdue)
            )])
        uncompleted_and_overdue = len([
            t for t in task_list if not t['completed'] and num_curr_date >= int(
                ''.join(t['due_date'].strftime(DATETIME_STRING_FORMAT).split('-'))
                )
            ])
        perc_incomplete = 0 if num_tasks == 0 else round(((uncompleted/num_tasks) * 100)) # Avoid ZeroDivisionError
        perc_overdue = 0 if num_tasks == 0 else round(((overdue/num_tasks) * 100))
        # I do not know if those overdue tasks have to also be incomplete

        print()
        disp_str = 'Task Overview:\n\n'
        disp_str += f'Total number of tasks: \t\t\t\t\t\t\t\t {num_tasks}\n'
        disp_str += f'Total number of completed tasks: \t\t\t\t\t {completed}\n'
        disp_str += f'Total number of uncompleted tasks: \t\t\t\t\t {uncompleted}\n'
        disp_str += f'Total number of uncompleted and overdue tasks: \t\t {uncompleted_and_overdue}\n'
        disp_str += f'Percentage of incomplete tasks: \t\t\t\t\t {perc_incomplete}%\n'
        disp_str += f'Percentage of overdue tasks: \t\t\t\t\t\t {perc_overdue}%'

        with open('task_overview.txt', 'w') as file:
            file.write(disp_str)

        num_users = len(username_password.keys())

        # For users.txt
        disp_str = 'User Overview:\n\n'
        disp_str += f'Total number of users: \t\t\t\t\t\t\t {num_users}\n'
        disp_str += f'Total number of tasks: \t\t\t\t\t\t\t {num_tasks}\n'
        for user in username_password.keys():
            # Naming Variables for each user to user_overview.txt
            tasks = [t for t in task_list if t['username'] == user]
            total_tasks = len(tasks)
            perc_total_tasks = 0 if num_tasks == 0 else round(((total_tasks/num_tasks) * 100))
            completed = len([t for t in tasks if t['completed']])
            perc_complete = 0 if total_tasks == 0 else round(((completed/total_tasks) * 100))
            perc_incomplete = 0 if total_tasks == 0 else 100 - perc_complete # Should be 0 if no tasks are given
            uncompleted_and_overdue = len([
                t for t in tasks if not t['completed'] and num_curr_date >= int(
                    ''.join(t['due_date'].strftime(DATETIME_STRING_FORMAT).split('-'))
                    )
                ])
            perc_uncompleted_and_overdue = 0 if total_tasks == 0 else round(((uncompleted_and_overdue/total_tasks) * 100))

            disp_str += f'\n{user}\n'
            disp_str += f'Total number of tasks: \t\t\t\t\t\t\t {total_tasks}\n'
            disp_str += f'Percentage of tasks assigned to user: \t\t\t {perc_total_tasks}%\n'
            disp_str += f'Percentage of completed tasks: \t\t\t\t\t {perc_complete}%\n'
            disp_str += f'Percentage of uncompleted tasks: \t\t\t\t {perc_incomplete}%\n'
            disp_str += f'Percentage of uncompleted and overdue tasks: \t {perc_uncompleted_and_overdue}%\n'
        
        with open('user_overview.txt', 'w') as file:
            file.write(disp_str)
        
        print('Generated onto task_overview.txt and user_overview.txt')

    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        if not os.path.exists("user_overview.txt") or not os.path.exists("task_overview.txt"):
            print("Your required files do not exist yet. Please type 'gr' to generate them.")
        else:
            print("--------------------------------------------")
            print()
            with open('task_overview.txt', 'r') as file:
                for line in file:
                    split = line.split('\t')  # Removing tabs (they are arranged on terminal different to textfile)
                    title = split[0].strip()
                    num = split[-1].strip()
                    print(title) if len(split) <= 1 else print(title, num)  # If statement occurs for heading
            print()
            print("--------------------------------------------")
            print()
            with open('user_overview.txt', 'r') as file:
                for line in file:
                    split = line.split('\t')
                    title = split[0].strip()
                    num = split[-1].strip()
                    print(title) if len(split) <= 1 else print(title, num)
            print()
            print("--------------------------------------------")

    elif menu == 'ds' and curr_user != 'admin':
        print('Only admins can access this option.')

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice. Please try again")
