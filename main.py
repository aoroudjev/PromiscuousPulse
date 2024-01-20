import driver_handler
import web_handler

import time
import tkinter as tk
from tkinter import ttk
from threading import Thread

import chromedriver_autoinstaller

webdriver_path = chromedriver_autoinstaller.install(path="./")
credentials = {}


def update_entry_state(state) -> None:
    username_entry.configure(state=state)
    password_entry.configure(state=state)
    first_check.configure(state=state)
    start_button.configure(state=state)


def update_options_state(state) -> None:
    dailies_button.configure(state=state)
    weeklies_button.configure(state=state)
    monthlies_button.configure(state=state)
    all_button.configure(state=state)


def run_thread(event=None) -> None:
    update_entry_state('disabled')
    global credentials
    credentials = {
        'username': username_entry.get(),
        'password': password_entry.get(),
    }
    Thread(target=full_sequence).start()


def full_sequence():
    # TODO: Change to separate events for button functionality or remove buttons?
    update_status('ORANGE', 'Starting Driver...')
    driver = driver_handler.start_driver()
    # driver.implicitly_wait(10) # potentially activate to remove some time.sleep(x)'s
    driver.set_window_size(100, 500)
    update_status('ORANGE', 'Logging In')
    try:
        web_handler.login(driver, credentials)
        update_status('GREEN', 'Success...Ready.')
    except ValueError:
        driver.close()
        update_status('RED', 'Login Failed')
        update_entry_state('normal')
    update_options_state('normal')

    # Actions of driver
    web_handler.do_cards(driver)
    # web_handler.track_habits(driver)
    # web_handler.do_assessment(driver)


def update_status(color, text) -> None:
    status_label.configure(fg=color.upper(), text=text.upper())


def enter_send(event):
    pass


root = tk.Tk()
root.title('Pulse')
root.geometry('220x200')
root.resizable(width=False, height=False)

root.bind('<Return>', run_thread)

# Credentials
username_label = tk.Label(root, text="Username:")
username_label.grid(column=0, row=0, sticky=tk.E)
username_entry = tk.Entry(root, width=25)
username_entry.insert(0, "aoroudjev@wyatt.com")
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
first_check = tk.Checkbutton(root, text='First Login', variable=first_var, borderwidth=2, relief='solid')
first_check.grid(column=0, row=3, columnspan=2, sticky=tk.W)

# Options
option_lf = tk.LabelFrame(root, text='Options')
option_lf.grid(column=0, row=5, padx=2, columnspan=3)

dailies_button = tk.Button(option_lf, text='Dailies', state='disabled', command="")
dailies_button.grid(column=0, row=0, padx=5, pady=5)
weeklies_button = tk.Button(option_lf, text='Weeklies', state='disabled', command="")
weeklies_button.grid(column=1, row=0, padx=5, pady=5)
monthlies_button = tk.Button(option_lf, text='Monthlies', state='disabled', command="")
monthlies_button.grid(column=2, row=0, padx=5, pady=5)
all_button = tk.Button(option_lf, text='ALL', state='disabled', command="")
all_button.grid(column=1, row=1, padx=5, pady=5)

root.mainloop()
