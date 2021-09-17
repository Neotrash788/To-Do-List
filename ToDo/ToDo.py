from datetime import datetime, timedelta
import pickle
import os

now = datetime.now()


class Task:
    def __init__(self, desc, due_date, prio):
        self.desc = desc
        self.prio = prio
        self.status = "Pending"
        self.due = due_date

    def get_desc(self):
        return self.desc

    def get_due_date(self):
        return self.desc

    def get_prio(self):
        return self.prio

    def is_pending(self):
        if self.status == 'Pending':
            return True
        else:
            return False

    def set_complete(self):
        self.status = 'Complete!'

    def set_prio(self, newPrio):
        self.prio = newPrio

    def is_pastdue(self):
        if datetime.now() < self.due:
            return True
        else:
            return False

    def get_daysleft(self):
        today = datetime.now()
        diff = self.due - today
        return diff.days

    def __repr__(self):
        if self.is_pending():
            days = self.get_daysleft()
            if self.is_pastdue():
                return f'Task {self.desc} is overdue by {abs(days)+1} days. (Prioratey {self.prio})'
            else:
                return f'Task {self.desc} is due in {days+1} days. (Prioratey {self.prio})'
        else:
            return f'Task {self.desc} is complete!'


def print_tasks(tasks, pending_only=True):
    for task in tasks:
        print(task)


tasks = []  # empty list to store all my tasks

tasks = []  # empty list to store all my tasks
tasks_filename = "tasks.dat"
# If existing tasks have been saved to a file, load that information
if os.path.exists(tasks_filename):
    with open(tasks_filename, "rb") as f:
        tasks = pickle.load(f)
action = ""


action = ""
while action != "exit":
    print("")
    print("*** WELCOME TO TASK MANAGER ***")
    print_tasks(tasks)
    print("")
    print("Your options...\nnew = Create new task\nclose = Close existing task\nexit = Quit the program")
    action = input("> ")

    if action == "new":
        desc = input("New task description: ")

        due = input("New task due date: ")
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        if due.lower()[:3] in days:
            due = now.weekday - days.index(due)
            print(due)
        else:
            try:
                due = datetime.strptime(due, "%d/%m/%Y")
            except ValueError:
                pass

        prio = input('prio:')
        new_task = Task(desc, due, prio)
        tasks.append(new_task)

    if action == "close":
        close_num = int(input("Enter task number to close: "))
        tasks[close_num].set_complete()

with open(tasks_filename, "wb") as f:
    pickle.dump(tasks, f)
