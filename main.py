from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
    password_list += (random.choice(symbols) for _ in range(nr_symbols))
    password_list += (random.choice(letters) for _ in range(nr_letters))
    password_list += (random.choice(numbers) for _ in range(nr_numbers))

    random.shuffle(password_list)
    password = ''.join(char for char in password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def _delete_entries():
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    website_entry.focus()


def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops!", message="Please don't leave any field empty!")
        return

    enter_data = messagebox.askokcancel(title="Check Your Entry", message=f"Website: {website}\nEmail: {email}"
                                                                          f"\nPassword: {password}\nSave password?")
    if enter_data:
        new_data = {
            website: {
                "Email": email,
                "Password": password
            }
        }
        try:
            passwords_file = open("passwords.json", "r")
            data = json.load(passwords_file)
        except FileNotFoundError:
            passwords_file = open("passwords.json", "w")
            json.dump(new_data, passwords_file, indent=4)
        else:
            data.update(new_data)
            passwords_file = open("passwords.json", "w")
            json.dump(data, passwords_file, indent=4)
        passwords_file.close()
        _delete_entries()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    try:
        with open("passwords.json", "r") as passwords_file:
            data = json.load(passwords_file)
            website = website_entry.get()
            if len(website) == 0:
                messagebox.showwarning(title="Oops!", message="Please enter website to search!")
                return
            email = data[website]["Email"]
            password = data[website]["Password"]
    except FileNotFoundError:
        open("passwords.json", "w")
        messagebox.showerror(title="Passwords File Not Found", message="Passwords file was not detected. New "
                                                                       "passwords file created.")
    except KeyError:
        messagebox.showerror(title="Password Not Found", message="Website Password Not Found")
    else:
        messagebox.showinfo(title="Password Search Complete", message=f"Email: {email}\nPassword: {password}")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()

window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
my_pass_logo = PhotoImage(file="logo.png")
logo = canvas.create_image(100, 100, image=my_pass_logo)
canvas.grid(row=0, column=1)

website_entry_label = Label(text="Website: ")
website_entry_label.grid(row=1, column=0)

website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(row=1, column=1)

search_password_button = Button(text="Search", width=10, command=find_password)
search_password_button.grid(row=1, column=2)

email_entry_label = Label(text="Email/Username:")
email_entry_label.grid(row=2, column=0)

email_entry = Entry(width=35)
email_entry.insert(0, "chethanbhaskar016@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)

password_entry_label = Label(text="Password:")
password_entry_label.grid(row=3, column=0)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

generate_password_button = Button(text="Generate Password", width=10, command=generate_password)
generate_password_button.grid(row=3, column=2)

add_password_button = Button(text="Add", width=33, command=save_password)
add_password_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
