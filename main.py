import driver_handler
import web_handler

import time
import tkinter as tk
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
        'Username': username_entry.get(),
        'Password': password_entry.get(),
    }
    Thread(target=full_sequence).start()




def full_sequence():
    update_status('ORANGE', 'Starting Driver...')
    driver = driver_handler.start_driver()
    update_status('GREEN', 'Logging In')
    web_handler.login(driver)


def update_status(color, text) -> None:
    status_label.configure(fg=color.upper(), text=text.upper())


root = tk.Tk()
root.title('PromiscuousPulse')
root.geometry('200x100')
root.resizable(width=False, height=False)

username_label = tk.Label(root, text="Username:")
username_label.grid(column=0, row=0, sticky=tk.W)
username_entry = tk.Entry(root)
username_entry.insert(0, "@wyatt.com")
username_entry.grid(column=1, row=0)

password_label = tk.Label(root, text="Password:")
password_label.grid(column=0, row=1, sticky=tk.W)
password_entry = tk.Entry(root, show="*")  # Password is hidden
password_entry.grid(column=1, row=1)

start_button = tk.Button(root, text='START', command=run_thread, width=20)
start_button.grid(column=0, row=3, columnspan=2)

status_label = tk.Label(root, fg='GREEN', text='READY', font='Bold')
status_label.grid(column=0, row=4, columnspan=2)

root.mainloop()
