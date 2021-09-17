import pickle
import time
import nice
from datetime import datetime, timedelta


class Task:
    def setDate(self, Input):
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        now = datetime.now()
        now = datetime.now()
        nextWeek = False

        if Input.lower().find('next') != -1:
            Input = Input[5:]
            nextWeek = True
        print(Input)
        if Input.lower()[:3] in days:
            weekday = days.index(Input.lower()[:3])
            currentWeekday = now.strftime('%w')
            diffDays = weekday-int(currentWeekday)+1
            due = now + timedelta(days=diffDays)

            if nextWeek:
                due = due + timedelta(days=7)

            print(due)
            self.due = due
        elif Input.find('/') != -1:
            try:
                due = datetime.strptime(Input, '%d/%m/%Y')
                self.due = due
            except Exception:
                print('----------------------------------------------------')
                print('Does not match format DD/MM/YYYY \n Please Try again')
                self.setDate(input('->'))
        else:
            print('----------------------------------------------------')
            print(
                f'Please Enter a valid weekday\nDate - DD/MM/YYYY\nWeekday - mon-sun\nNext week - next mon-sun')
            self.setDate(input('->'))

    def __init__(self, sub, content, due, prio, comp=False):
        self.sub = sub
        self.content = content
        self.setDate(due)
        self.prio = prio
        self.comp = comp

    def setSub(self, Input):
        self.sub = Input

    def setContent(self, Input):
        self.content = Input

    def setPrio(self, Input):
        self.prio = Input

    def setComp(self):
        if self.comp == False:
            self.comp = True
        else:
            self.comp = False

    def getPrio(self):
        return self.prio

    def getContent(self):
        return self.content

    def getSubject(self):
        return self.sub

    def getDue(self):
        diff = self.due - datetime.now()
        return diff.days+1

    def getComp(self):
        if self.comp == True:
            return 'Complete'
        else:
            return 'Not Complete'

    def getLen(self):
        sub = self.sub
        content = self.content
        due = self.due
        prio = self.prio
        comp = self.getComp()
        return len(f'{sub}{content}{due}{prio}{comp}')

    def __repr__(self):
        sub = self.sub
        content = self.content
        due = self.getDue()
        if due < 0:
            due = f'(overdue by {abs(int(due))} days)'
        elif due == 0:
            due = '(due today)'
        else:
            due = f'in {due} days'
        prio = self.prio
        comp = self.getComp()
        return(f'For {sub} you have to {content} {due} days, priorotey({prio}) - {comp}')


try:
    with open('Tasks.dat', 'rb') as f:
        tasks = list(pickle.load(f))
except EOFError:
    tasks = []  # No tasks in file


def printTasks():
    for i in tasks:
        if type(i) != str:
            if i.getComp() == 'Complete' and hide == True:
                pass
            else:
                print(i)
        else:
            print(i)


def removeTask(task):
    try:
        tasks.pop(task)
    except Exception as e:
        print(f'Task no.{task + 1} does not exist')


def completeTask(task):
    try:
        tasks[task].setComp()
    except Exception as e:
        print('Index not in tasks')


def sort(by):
    global headingPoss, tasks
    change = True
    sortable = True
    headings = True
    arr = []
    prev = 0
    by = by.lower()[:3]

    for i in range(len(tasks)-1, -1, -1):
        if type(tasks[i]) == str:
            tasks.pop(i)

    if by == 'sub':
        change = False
        headings = False
        sortable = False
        subjects = []
        for i in range(0, len(tasks)):
            for ii in subjects:
                if f'__________{tasks[i].getSubject()}__________' in ii:
                    ii.append(i)
                    break
            else:
                subjects.append(
                    [f'__________{tasks[i].getSubject()}__________', i])

        print(subjects)

        sortedArr = []
        for i in subjects:
            sortedArr.append(i[0])
            for ii in range(1, len(i)):
                sortedArr.append(tasks[i[ii]])

    if by == 'pri':
        for i in range(0, len(tasks)):
            arr.append(f'{i}/{tasks[i].getPrio()}')

    if by == 'len':
        headings = False
        for i in range(0, len(tasks)):
            arr.append(f'{i}/{tasks[i].getLen()}')

    if by == 'due':
        for i in range(0, len(tasks)):
            diffDue = tasks[i].getDue()
            arr.append(f'{i}/{diffDue}')

    if by == 'non':
        sortable = False

    # implement check for mutiple digits
    if sortable:
        for i in range(0, len(arr)):
            for ii in range(0, len(arr)-1):
                slash = arr[ii].find('/')
                if arr[ii][slash:] > arr[ii+1][slash:]:
                    arr[ii], arr[ii+1] = arr[ii+1], arr[ii]

    if headings:
        sortedArr = []
        if sortable == True:
            for i in arr:
                slash = i.find('/')+1
                if prev != i[slash:]:
                    sortedArr.append(f'__________{i[slash:]}__________')
                    prev = i[slash:]
                sortedArr.append(tasks[int(i[:slash-1])])
        if by in ['pri', 'non', 'due']:
            tasks = sortedArr
        else:
            print(f'Unable to sort by {by}')
    elif change:
        sortedArr = []
        for i in arr:
            slash = i.find('/')+1
            sortedArr.append(tasks[int(i[:slash-1])])
        tasks = sortedArr
    else:
        tasks = sortedArr


def accountForHeadings(Input):
    global headingPoss
    headingPoss = []
    for i in range(0, len(tasks)):
        if type(tasks[i]) == str:
            headingPoss.append(i)

    print(headingPoss)
    if Input in headingPoss:
        return Input + 1
    elif len(headingPoss) > 0:
        return Input + 1
    else:
        return Input


def Help():
    print('''
    ----------------------------------------------------
    Your choices:
    new,add -> creates new task
    sort,arrange -> sorts all tasks
    pop,remove,del -> removes a task
    hide,show -> shows or hides completed tasks
    finish,complete -> Marks a cetrian task as complete
    
    (Only the first 3 chariters are required)

    Sort:
    due
    none
    length
    subject
    ----------------------------------------------------
    ''')


print('Type help for help')
time.sleep(1)
# Loop
run = True
hide = False
while run:

    global headingPoss
    print('----------------------------------------------------')
    printTasks()
    print('----------------------------------------------------')
    choice = input('Choice ->')[:3]
    choice = choice.lower()

    if choice == 'hel':
        Help()

    if choice in ['new', 'add']:
        sub = input('subject ->')
        content = input('Content ->')
        due = input('Due ->')
        prio = input('Prioratey ->')
        comp = False
        newTask = Task(sub, content, due, prio, comp)
        tasks.append(newTask)

    if choice in ['rem', 'pop', 'del']:
        try:
            remove = int(input('Which task would you like to remove ->'))-1
        except ValueError:
            print('Must be a valid integer')
            continue
        if remove > 0:
            removeTask(accountForHeadings(remove))
        else:
            print('Must be above 0')

    if choice in ['fin', 'com']:
        try:
            completeTask(accountForHeadings(
                int(input('Which Task would you like to mark as complete ->'))-1))
        except Exception as e:
            print('Must be numeric', e)
    if choice in ['sor', 'arr']:
        sort(input('Sort by ->'))

    if choice in ['hid', 'sho']:
        if hide == False:
            hide = True
        else:
            hide = False

    if choice in ['end', 'sto', 'exi', 'clo']:
        run = False

    if choice == 'cle':
        nice.draw()
        input('press any key to end')
        exit()


with open('Tasks.dat', 'wb') as f:
    pickle.dump(tasks, f)
