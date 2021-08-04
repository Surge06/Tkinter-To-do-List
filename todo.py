import tkinter as tk
import datetime as dt
from tkinter import messagebox as mb


class to_do:
    def __init__(self):
        self.root = tk.Tk()  # assigning tkinter to this variable
        self.root.title('Python To-Do List')  # title
        self.root.configure(background='white')  # background for app

        self.header = tk.Label(text='ToDo List', font='bold', bg='white')  # header background
        self.entry_task = tk.Entry(self.root)  # entry one
        self.entry_start = tk.Entry(self.root)  # entry two
        self.entry_due = tk.Entry(self.root)  # entry three
        self.entry_priority = tk.Entry(self.root)  # entry four

        self.completed_tasks = {'task': [], 'start': [], 'due': [], 'priority': [],
                                'completed': []}  # list where completed tasks go
        self.custom_reminders = {'task': [], 'date': []}  # custom reminders column
        self.dict_list = {'index': [], 'task': [], 'start': [], 'due': [], 'priority': [],
                          'status': []}  # main dictionary list with task details
        self.all_tasks = tk.Listbox(self.root, relief='solid', bd=1, selectmode='multiple',
                                    width=80)  # listbox that simplifies task details

        self.headings = ['Description', 'Start Date', 'Due Date', 'Priority']  # headings for labels
        self.header.grid(row=0, column=0, columnspan=2, sticky='nsew')  # setting up headings in layout
        for i in range(0, 4):
            tk.Label(self.root, text=self.headings[i], bg='white').grid(row=i + 1, column=1, sticky='w')

        # buttons for functions, to add, modify, mark complete or to delete.
        # The others are to view reminders or add a custom one.
        self.add = tk.Button(self.root, text='Add', bg='white', activebackground='black', activeforeground='white',
                             bd=1, relief='solid', command=self.add_task)
        self.modify = tk.Button(self.root, text='Modify', bg='white', activebackground='black',
                                activeforeground='white', bd=1, relief='solid', command=self.modify_task)
        self.add_rem = tk.Button(self.root, text='Add Reminder', bg='white', activebackground='black',
                                 activeforeground='white', bd=1, relief='solid', command=self.custom_reminder)
        self.view_rem = tk.Button(self.root, text='View reminders', bg='white', activebackground='black',
                                  activeforeground='white', bd=1, relief='solid', command=self.view_reminders)
        self.comp_sel = tk.Button(self.root, text='Complete Marked', bg='white', activebackground='black',
                                  activeforeground='white', bd=1, relief='solid', command=self.complete_task)
        self.comp_all = tk.Button(self.root, text='Complete All', bg='white', activebackground='black',
                                  activeforeground='white', bd=1, relief='solid', command=self.complete_all)
        self.del_sel = tk.Button(self.root, text='Delete Marked', bg='white', activebackground='black',
                                 activeforeground='white', bd=1, relief='solid', command=self.remove_task)
        self.del_all = tk.Button(self.root, text='Delete All', bg='white', activebackground='black',
                                 activeforeground='white', bd=1, relief='solid', command=self.remove_all)

        self.main = tk.Label(self.root, text='Main Tasks', bg='white', relief='flat').grid(row=0, column=3)
        self.comp_list = tk.Button(self.root, text='View Complete Tasks', bg='white', activebackground='black',
                                   activeforeground='white', bd=1, relief='solid', width=10,
                                   command=self.complete).grid(row=0, column=4, sticky='nsew')

        self.entry_task.grid(row=1,
                             column=2)  # grid positioning for labels, and their respective entry boxes side by side
        self.entry_start.grid(row=2, column=2)
        self.entry_due.grid(row=3, column=2)
        self.entry_priority.grid(row=4, column=2)

        self.add.grid(row=6, column=1, sticky='nsew')  # first column of buttons
        self.modify.grid(row=7, column=1, sticky='nsew')
        self.add_rem.grid(row=8, column=1, sticky='nsew')
        self.view_rem.grid(row=9, column=1, sticky='nsew')

        self.comp_sel.grid(row=6, column=2, sticky='nsew')  # second column of buttons
        self.comp_all.grid(row=7, column=2, sticky='nsew')
        self.del_sel.grid(row=8, column=2, sticky='nsew')
        self.del_all.grid(row=9, column=2, sticky='nsew')

        self.all_tasks.grid(row=1, column=3, rowspan=11, columnspan=3, sticky='nsew')  # places the listbox

        self.test_data()  # premade data for testing
        self.populate_listbox()  # populates the listbox using data in dictionary
        self.reminder_check()  # calling function to test reminder function

    def add_task(self):
        if self.entry_task.get() == '':  # if statment used to check if the first entry box is empty
            pass
        else:
            self.row = len(self.dict_list['index']) + 1  # used to index
            self.dict_list['index'].append(self.row)  # appends the row index
            self.dict_list['task'].append(self.entry_task.get())  # appends the task description
            self.dict_list['start'].append(self.entry_start.get())  # appends the start date
            self.dict_list['due'].append(self.entry_due.get())  # appends the due date
            self.dict_list['priority'].append(self.entry_priority.get())  # appends priority level

            self.all_tasks.insert('end', '{}. {}. {}. {}. {} Priority'.format(  # adds task to the listbox
                self.dict_list['index'][-1],
                self.dict_list['task'][-1],
                self.dict_list['start'][-1],
                self.dict_list['due'][-1],
                self.dict_list['priority'][-1]))

    def modify_task(self):
        self.t = self.all_tasks.curselection()  # retrieves selected task and stores their indexes in a list
        self.top = tk.Toplevel()  # creates popup window
        self.top.configure(bg='white')
        self.top.title('Edit Task')

        tk.Label(self.top, text='Task:', bg='white').grid(row=1, column=0, columnspan=2,
                                                          sticky='w')  # setting up labels for modify function
        tk.Label(self.top, text='Start Date', bg='white').grid(row=2, column=0, columnspan=2, sticky='w')
        tk.Label(self.top, text='Due Date', bg='white').grid(row=3, column=0, columnspan=2, sticky='w')
        tk.Label(self.top, text='Priority', bg='white').grid(row=4, column=0, columnspan=2, sticky='w')

        self.task_edit = tk.StringVar(self.top,
                                      value=self.dict_list['task'][self.t[0]])  # stringvar used to store variables
        self.start_edit = tk.StringVar(self.top, value=self.dict_list['start'][self.t[0]])
        self.due_edit = tk.StringVar(self.top, value=self.dict_list['due'][self.t[0]])
        self.priority_edit = tk.StringVar(self.top, value=self.dict_list['priority'][self.t[0]])

        self.e1 = tk.Entry(self.top, textvariable=self.task_edit)  # inserting text into text box as examples
        self.e1.grid(row=1, column=2)
        self.e2 = tk.Entry(self.top, textvariable=self.start_edit)
        self.e2.grid(row=2, column=2)
        self.e3 = tk.Entry(self.top, textvariable=self.due_edit)
        self.e3.grid(row=3, column=2)
        self.e4 = tk.Entry(self.top, textvariable=self.priority_edit)
        self.e4.grid(row=4, column=2)

        # cancel button returns to main window,
        # save button stores information to dictionary
        # then returns to the main window
        tk.Button(self.top, text='Cancel', bg='white', activebackground='black', activeforeground='white', bd=1,
                  relief='solid', command=self.top.destroy).grid(row=5, column=0, sticky='nsew')
        tk.Button(self.top, text='Save', bg='white', activebackground='black', activeforeground='white', bd=1,
                  relief='solid', command=self.save_edit).grid(row=5, column=1, sticky='nsew')

    def save_edit(self):
        self.dict_list['task'][
            self.t[0]] = self.e1.get()  # get() used to retrieve new data, then replaces original value at the same time
        self.dict_list['start'][self.t[
            0]] = self.e2.get()  # modify function only uses the first selected value, as in the first item in the list
        self.dict_list['due'][self.t[0]] = self.e3.get()
        self.dict_list['priority'][self.t[0]] = self.e4.get()

        self.all_tasks.delete(self.t[0])  # deletes current list box entry, and replaces it with the updated one.
        self.all_tasks.insert(self.t[0], '{}. {}. {}. {}. {} Priority'.format(
            self.dict_list['index'][self.t[0]],
            self.dict_list['task'][self.t[0]],
            self.dict_list['start'][self.t[0]],
            self.dict_list['due'][self.t[0]],
            self.dict_list['priority'][self.t[0]]))
        self.top.destroy()

    def complete_task(self):
        self.select = self.all_tasks.curselection()  # masks tasks as completed by storing them in separate dictionary
        for i in self.select[::-1]:
            self.completed_tasks['task'].append(self.dict_list['task'][i])
            self.completed_tasks['start'].append(self.dict_list['start'][i])
            self.completed_tasks['due'].append(self.dict_list['due'][i])
            self.completed_tasks['priority'].append(self.dict_list['priority'][i])
            self.completed_tasks['completed'].append(self.today)

        self.select = self.all_tasks.curselection()
        for i in self.select[::-1]:  # removes tasks one by one, each time using last index of list
            del self.dict_list['index'][i]
            del self.dict_list['task'][i]
            del self.dict_list['start'][i]
            del self.dict_list['due'][i]
            del self.dict_list['priority'][i]

        self.dict_list['index'] = []  # empties index list the overwrites for unique indexes
        for i in range(1, len(self.dict_list['task']) + 1):
            self.dict_list['index'].append(i)

        self.all_tasks.delete(0, 'end')  # also empties the listbox
        self.populate_listbox()  # then repopulates it

    def complete_all(self):
        for i in range(0, len(self.dict_list['index'])):  # stores all tasks as complete then continues
            self.completed_tasks['task'].append(self.dict_list['task'][i])
            self.completed_tasks['start'].append(self.dict_list['start'][i])
            self.completed_tasks['due'].append(self.dict_list['due'][i])
            self.completed_tasks['priority'].append(self.dict_list['priority'][i])
            self.completed_tasks['completed'].append(self.today)

        self.all_tasks.delete(0, 'end')
        self.dict_list['index'] = []
        self.dict_list['task'] = []
        self.dict_list['start'] = []
        self.dict_list['due'] = []
        self.dict_list['priority'] = []

    def remove_task(self):
        self.confirm = mb.askyesno('Question', 'Do you want to delete the selected tasks?')
        if self.confirm == True:
            self.select = self.all_tasks.curselection()
            for i in self.select[::-1]:  # removes tasks one by one, each time using last index of list
                del self.dict_list['index'][i]
                del self.dict_list['task'][i]
                del self.dict_list['start'][i]
                del self.dict_list['due'][i]
                del self.dict_list['priority'][i]

            self.dict_list['index'] = []  # empties index list the overwrites for unique indexes
            for i in range(1, len(self.dict_list['task']) + 1):
                self.dict_list['index'].append(i)

            self.all_tasks.delete(0, 'end')  # also empties the listbox
            self.populate_listbox()  # then repopulates it
        else:
            pass

    def remove_all(self):
        self.confirm = mb.askyesno('Question', 'Do you want to delete all tasks?')
        if self.confirm == True:
            self.all_tasks.delete(0, 'end')  # empties listbox
            self.dict_list['index'] = []  # then empties dictionary
            self.dict_list['task'] = []
            self.dict_list['start'] = []
            self.dict_list['due'] = []
            self.dict_list['priority'] = []
        else:
            pass

    def reminder_check(self):
        self.today = dt.date.today().strftime('%d/%m/%Y')  # uses today's date formatted (dd/mm/yyyy)
        self.tasks_list = []  # separate list containing all tasks for this function
        self.due_check = []  # list containing days between two dates

        for i in range(0, len(self.dict_list['index'])):  # adds from dictionary
            self.tasks_list.append('{}. {}. {}. {}. {} Priority'.format(
                self.dict_list['index'][i],
                self.dict_list['task'][i],
                self.dict_list['start'][i],
                self.dict_list['due'][i],
                self.dict_list['priority'][i]))

        for i in range(0, len(self.dict_list['index'])):
            self.now = dt.datetime.strptime(self.today, '%d/%m/%Y')  # today's date
            self.duedate = dt.datetime.strptime(self.dict_list['due'][i], '%d/%m/%Y')  # due date per item in dictionary
            self.delta = self.duedate - self.now  # difference between the two days
            self.due_check.append(self.delta.days)  # appends days to list

        self.urgent_tasks = []  # blank list for tasks with one day or less
        for i in range(0, len(self.due_check)):
            if self.due_check[i] < 2:
                self.urgent_tasks.append(self.tasks_list[i])

        if len(self.urgent_tasks) > 0:  # if there are tasks that are urgent, the window appears
            self.reminder_window()

    def reminder_window(self):  # window with all reminders
        self.rem = tk.Toplevel()
        self.rem.title('Urgent Reminders!')
        self.rem.configure(bg='white')

        tk.Label(self.rem, text='You have the following tasks due:', bg='white').grid(row=0,
                                                                                      column=0)
        # label and listbox with urgent tasks
        self.rem_box = tk.Listbox(self.rem, width=80)
        # button to close window
        self.okay = tk.Button(self.rem, text='Okay', bg='white', activebackground='black', activeforeground='white',
                              bd=1, relief='solid', command=self.rem.destroy)

        for i in self.urgent_tasks:
            self.rem_box.insert('end', i)
        self.rem_box.grid(row=1, column=0)
        self.okay.grid(row=2, column=0)

    def test_data(self):  # test data for program
        self.dict_list['index'].append(1)
        self.dict_list['task'].append('Mow the lawn')
        self.dict_list['start'].append('08/05/2019')
        self.dict_list['due'].append('13/05/2019')
        self.dict_list['priority'].append('Low')

        self.dict_list['index'].append(2)
        self.dict_list['task'].append('Wash the dishes')
        self.dict_list['start'].append('08/05/2019')
        self.dict_list['due'].append('11/05/2019')
        self.dict_list['priority'].append('Medium')

        self.dict_list['index'].append(3)
        self.dict_list['task'].append('Finish coursework')
        self.dict_list['start'].append('09/05/2019')
        self.dict_list['due'].append('11/05/2019')
        self.dict_list['priority'].append('High')

        self.dict_list['index'].append(4)
        self.dict_list['task'].append('Make a todo list')
        self.dict_list['start'].append('09/05/2019')
        self.dict_list['due'].append('12/05/2019')
        self.dict_list['priority'].append('High')

        self.dict_list['index'].append(5)
        self.dict_list['task'].append('Watch Avengers: Endgame')
        self.dict_list['start'].append('09/05/2019')
        self.dict_list['due'].append('14/05/2019')
        self.dict_list['priority'].append('Low')

    def custom_reminder(self):  # popup window for reminders
        self.answer = mb.askyesno('Question', 'Do you want to set a reminder?')  # confirmation message
        if self.answer == True:  # loads a window to enter custom reminder functions, then adds to a separate list
            self.remb = tk.Toplevel()
            self.remb.title('Set Reminder')
            self.remb.configure(bg='white')

            self.rem_entry = tk.Entry(self.remb, width=30)  # entry boxes and labels for window
            self.date_entry = tk.Entry(self.remb, width=30)
            self.rem_entry.insert(0, 'Enter a task')
            self.date_entry.insert(0, 'Enter a date (i.e. 1/7/2017)')

            self.save_rem = tk.Button(self.remb, text='Save', bg='white', activebackground='black',
                                      activeforeground='white', bd=1, relief='solid', command=self.save_reminder)
            self.cancel = tk.Button(self.remb, text='Cancel', bg='white', activebackground='black',
                                    activeforeground='white', bd=1, relief='solid', command=self.remb.destroy)
            self.rem_entry.grid(row=0, column=0, columnspan=2, padx=5)

            self.date_entry.grid(row=1, column=0, columnspan=2)
            self.save_rem.grid(row=3, column=0, sticky='nsew', padx=5)
            self.cancel.grid(row=3, column=1, sticky='nsew')
        else:  # if the user cancels, returns to main window
            pass

    def save_reminder(self):
        self.custom_reminders['task'].append(self.rem_entry.get())
        self.custom_reminders['date'].append(self.date_entry.get())
        mb.showinfo('Information', 'Reminder set.')  # confirmation that the message was added
        self.remb.destroy()

    def view_reminders(self):
        self.custom_rem = tk.Toplevel()
        self.custom_rem.title('All Reminders')
        self.custom_rem.configure(bg='white')

        self.rem_box_two = tk.Listbox(self.custom_rem, width=80)  # listbox for custom reminders
        if self.custom_reminders['task'] != '':  # if the entry box is not blank, adds all custom reminders to a listbox
            for i in range(0, len(self.custom_reminders['task'])):
                self.rem_box_two.insert('end', '{}, Due:{}'.format(self.custom_reminders['task'],
                                                                   self.custom_reminders['date']))
            tk.Label(self.custom_rem, text='Your Reminders:', bg='white').grid(row=0, column=0)
            self.rem_box_two.grid(row=1, column=0)
        # close button
        tk.Button(self.custom_rem, text='Close', bg='white', activebackground='black', activeforeground='white', bd=1,
                  relief='solid', command=self.custom_rem.destroy).grid(row=2, column=0)

        self.reminder_check()

    def populate_listbox(self):  # populates the listbox using dictionary
        for i in range(0, len(self.dict_list['index'])):
            self.all_tasks.insert('end', '{}. {}. {}. {}. {} Priority'.format(
                self.dict_list['index'][i],
                self.dict_list['task'][i],
                self.dict_list['start'][i],
                self.dict_list['due'][i],
                self.dict_list['priority'][i]))

    def complete(self):
        self.comp_window = tk.Toplevel()
        self.comp_window.title('Completed tasks')
        self.comp_window.configure(bg='white')
        self.comp_headings = ['Task', 'Start', 'Due', 'Priority', 'Completed']
        for i in range(0, len(self.comp_headings)):
            tk.Label(self.comp_window, text=self.comp_headings[i], bg='white', font='bold').grid(row=1, column=i,
                                                                                                 sticky='w')
        for i in range(0, len(self.completed_tasks['task'])):
            tk.Label(self.comp_window, text=self.completed_tasks['task'][i], bg='white').grid(row=i + 2, column=0,
                                                                                              sticky='w')
            tk.Label(self.comp_window, text=self.completed_tasks['start'][i], bg='white').grid(row=i + 2, column=1,
                                                                                               sticky='w')
            tk.Label(self.comp_window, text=self.completed_tasks['due'][i], bg='white').grid(row=i + 2, column=2,
                                                                                             sticky='w')
            tk.Label(self.comp_window, text=self.completed_tasks['priority'][i], bg='white').grid(row=i + 2, column=3,
                                                                                                  sticky='w')
            tk.Label(self.comp_window, text=self.completed_tasks['completed'][i], bg='white').grid(row=i + 2, column=4,
                                                                                                   sticky='w')
        tk.Button(self.comp_window, text='Close', bg='white', activebackground='black', activeforeground='white', bd=1,
                  relief='solid', command=self.comp_window.destroy).grid(row=7, column=4)


main = to_do()
