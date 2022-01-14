from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # select random letters, numbers and symbols
    nr_letters_list = [choice(letters) for char in range(randint(8, 10))]
    nr_symbols_list = [choice(symbols) for char in range(randint(2, 4))]
    nr_numbers_list = [choice(numbers) for char in range(randint(2, 4))]

    # join all lists, shuffle the list, convert list to string
    password_list_1 = nr_numbers_list + nr_symbols_list + nr_letters_list
    shuffle(password_list_1)
    password = "".join(password_list_1)
    #print(f"Your password is: {password}")

    # insert password into password entry at 0th character and copy to clipboard
    entry_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_password():
    # retrieve information from entry
    website = str(entry_website.get())
    username = str(entry_username.get())
    password = str(entry_password.get())
    # add information to dictionary
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    # checking for blank field entries
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="It appears you have left one or more fields blank, please complete all fields")
    else:
        is_ok = messagebox.askokcancel(title="Confirm Details", message=f"Are all details correct\n Website: {website}\n Email: {username}\n Password: {password}")

        if is_ok:
            try:
                # open and write password details
                with open("password_data.json", "r") as data_file:
                    # read old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("password_data.json", "w") as data_file:
                    # saving updated data
                    json.dump(new_data, data_file, indent=4)
            else:
                # update old data with new data
                data.update(new_data)

                with open("password_data.json", "w") as data_file:
                    # saving updated data
                    json.dump(data, data_file, indent=4)

            finally:
                # clear entries
                entry_website.delete(0, END)
                entry_password.delete(0, END)
                entry_username.delete(0, END)


# ---------------------------- Find Password ------------------------------- #


def find_password():
    # get password
    website = str(entry_website.get())
    try:
        # open json file and read data
        with open("password_data.json", "r") as data_file:
            # read old data
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No Data File Found")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Account Info", message=f"Your username is: {email}\n Your password is: {password}")
        else:
            messagebox.showinfo(title="Oops", message=f"No Details for {website} Exist")


# ---------------------------- UI SETUP ------------------------------- #
# create window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


# create canvas
canvas = Canvas(width=200, height=200)
padlock_img = PhotoImage(file="/Users/harry/PycharmProjects/day29PasswordManager/logo.png")
canvas.create_image(100, 100, image=padlock_img)
canvas.grid(column=1, row=0)

# create label
website_label = Label(text="Website", font="Arial")
website_label.grid(column=0, row=1)
#website_label.config(padx=5, pady=5)

username_label = Label(text="Username/Email", font="Arial")
username_label.grid(column=0, row=2)
#username_label.config(padx=5, pady=5)

password_label = Label(text="Password", font="Arial")
password_label.grid(column=0, row=3)
#password_label.config(padx=5, pady=5)

# create button
generate_password_button = Button(text="Generate Password", font="Arial", command=generate_password)
generate_password_button.grid(column=2, row=3)
#generate_password_button.config(padx=5, pady=5)

add_button = Button(text="Add", font="Arial", width=33, command=add_password)
add_button.grid(column=1, row=4, columnspan=2)
#add_button.config(padx=5, pady=5)

search_button = Button(text="Search", font="Arial", command=find_password)
search_button.grid(column=2, row=1)
#generate_password_button.config(padx=5, pady=5)

# create entry
entry_website = Entry(width=30)
entry_website.grid(column=1, row=1, columnspan=1)
entry_website.focus()
entry_username = Entry(width=60)
entry_username.grid(column=1, row=2, columnspan=2)

entry_password = Entry(width=25)
entry_password.grid(column=1, row=3)

# keep GUI up on screen
window.mainloop()
