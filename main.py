import driver_handler
import web_handler

import time
import tkinter as tk
from tkinter import ttk
from threading import Thread

import chromedriver_autoinstaller
from selenium.common import WebDriverException

webdriver_path = chromedriver_autoinstaller.install(path="./")
credentials = {}


def update_entry_state(state) -> None:
    username_entry.configure(state=state)
    password_entry.configure(state=state)
    start_button.configure(state=state)


def run_thread() -> None:
    update_entry_state('disabled')
    global credentials
    credentials = {
        'username': username_entry.get(),
        'password': password_entry.get(),
    }
    Thread(target=full_sequence).start()


def full_sequence():
    update_status('ORANGE', 'Starting Driver...')
    driver = driver_handler.start_driver()
    driver.set_window_size(100, 500)
    update_status('ORANGE', 'Logging In')
    try:
        web_handler.login(driver, credentials)
        update_status('GREEN', 'Success')
    except ValueError:
        driver.close()
        update_status('RED', 'Login Failed')
        update_entry_state('normal')


def update_status(color, text) -> None:
    status_label.configure(fg=color.upper(), text=text.upper())


root = tk.Tk()
root.title('PromiscuousPulse')
root.geometry('220x200')
root.resizable(width=False, height=False)

# Credentials
username_label = tk.Label(root, text="Username:")
username_label.grid(column=0, row=0, sticky=tk.E)
username_entry = tk.Entry(root, width=25)
username_entry.insert(0, "@wyatt.com")
username_entry.grid(column=1, row=0)

password_label = tk.Label(root, text="Password:")
password_label.grid(column=0, row=1, sticky=tk.E)
password_entry = tk.Entry(root, show="*", width=25)  # Password is hidden
password_entry.grid(column=1, row=1)

# Control Buttons
start_button = tk.Button(root, text='START', command=run_thread, width=15)
start_button.grid(column=1, row=3, columnspan=2)

status_label = tk.Label(root, fg='GREEN', text='READY', font='BOLD', borderwidth=1, relief='ridge', bg='WHITE',
                        width=25)
status_label.grid(column=0, row=4, columnspan=2)

first_var = tk.BooleanVar()
first_check = tk.Checkbutton(root, text='First Time', variable=first_var, borderwidth=2, relief='solid')
first_check.grid(column=0, row=3, columnspan=2, sticky=tk.W)

# Options
option_lf = ttk.LabelFrame(root, text='Options')
option_lf.grid(column=0, row=5, padx=2, columnspan=3)

dailies_check = tk.Button(option_lf, text='Dailies', state='disabled')
dailies_check.grid(column=0, row=0, padx=5, pady=5)
weeklies_check = tk.Button(option_lf, text='Weeklies', state='disabled')
weeklies_check.grid(column=1, row=0, padx=5, pady=5)
monthlies_check = tk.Button(option_lf, text='Monthlies', state='disabled')
monthlies_check.grid(column=2, row=0, padx=5, pady=5)
root.mainloop()
