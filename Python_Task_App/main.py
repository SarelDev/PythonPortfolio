import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import json

class TaskManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")

        self.calendar = ttk.Treeview(master)
        self.calendar['columns'] = ('Category', 'Description', 'Date Created', 'Due Date')
        self.calendar.heading("#0", text="Date")
        self.calendar.column("#0", width=150)
        self.calendar.heading('Category', text='Category')
        self.calendar.column('Category', width=100)
        self.calendar.heading('Description', text='Description')
        self.calendar.column('Description', width=200)
        self.calendar.heading('Date Created', text='Date Created')
        self.calendar.column('Date Created', width=120)
        self.calendar.heading('Due Date', text='Due Date')
        self.calendar.column('Due Date', width=120)
        self.calendar.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        self.categories = ttk.Combobox(master, values=["Work", "Personal", "Study"])
        self.categories.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

        self.desc_label = ttk.Label(master, text="Description:")
        self.desc_label.grid(row=1, column=1, padx=10, pady=5)

        self.desc_entry = ttk.Entry(master)
        self.desc_entry.grid(row=1, column=2, padx=10, pady=5, sticky='ew')

        self.due_label = ttk.Label(master, text="Due Date:")
        self.due_label.grid(row=1, column=3, padx=10, pady=5)

        self.due_entry = ttk.Entry(master)
        self.due_entry.grid(row=1, column=4, padx=10, pady=5, sticky='ew')

        self.add_button = ttk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

        self.delete_button = ttk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

        self.save_button = ttk.Button(master, text="Save", command=self.save_tasks)
        self.save_button.grid(row=2, column=2, padx=10, pady=5, sticky='ew')

        self.load_tasks()

    def add_task(self):
        category = self.categories.get()
        description = self.desc_entry.get()
        due_date = self.due_entry.get()
        if not description:
            messagebox.showwarning("Warning", "Please enter a description.")
            return
        created_date = datetime.now().strftime('%Y-%m-%d')
        self.calendar.insert('', 'end', text=created_date, values=(category, description, created_date, due_date))
        self.desc_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)

    def delete_task(self):
        selected_item = self.calendar.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return
        self.calendar.delete(selected_item)

    def save_tasks(self):
        tasks = {}
        for child in self.calendar.get_children():
            date = self.calendar.item(child, 'text')
            category, description, created_date, due_date = self.calendar.item(child, 'values')
            tasks[date] = {'category': category, 'description': description, 'created_date': created_date, 'due_date': due_date}

        with open('tasks.json', 'w') as file:
            json.dump(tasks, file)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks = json.load(file)
            for date, task in tasks.items():
                category = task['category']
                description = task['description']
                created_date = task['created_date']
                due_date = task['due_date']
                self.calendar.insert('', 'end', text=created_date, values=(category, description, created_date, due_date))
        except FileNotFoundError:
            pass

def main():
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
