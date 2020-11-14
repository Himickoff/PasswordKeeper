from tkinter import *
import hashlib
from cryptography.fernet import Fernet
import shutil


#  Cryptography defines
def write_key():  # Create new crypto key
    key = Fernet.generate_key()
    with open('crypto.key', 'wb') as key_file:
        key_file.write(key)


def load_key():  # Load crypto key
    try:
        return open('crypto.key', 'rb').read()
    except:
        try:
            input_window("Missing key, create new?(input in Password yes or no)")
            if entryPassword.get() == "yes":
                write_key()
                input_window("New key create")
            else:
                input_window("Rejected")
        except:
            pass


def encrypt(filename, key):  # Encrypting file with key
    f = Fernet(key)
    with open(filename, 'rb') as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, 'wb') as file:
        file.write(encrypted_data)


def decrypt(filename, key):  # Decrypting file with key
    f = Fernet(key)
    try:
        with open(filename, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(filename, 'wb') as file:
            file.write(decrypted_data)
    except:
        file = open('mainFile.txt', 'w')
        file.close()


#  Function
def save():
    key = load_key()
    file1 = 'mainFile.txt'  # File with data
    try:
        decrypt(file1, key)
    except:  # if no file, create it
        file = open('mainFile.txt', 'w')
        file.close()
    save = "Login:" + entryLogin.get() + "  " + "Password:" + entryPassword.get() + ' ' + '(from' + ' ' + noticeEntry.get() + ')' + '\n'
    # Create variable with data from input
    file = open('mainFile.txt', 'a')
    file.write(save)
    file.close()
    encrypt(file1, key)
    input_window("Save done successful")


def show():  # Output passwords in panel(text)
    check = check_main_password()
    text = create_text()
    if check is True:
        key = load_key()
        file = 'mainFile.txt'
        decrypt(file, key)
        text.delete('1.0', END)
        text1 = output_password()
        text.insert(0.0, text1)
        encrypt(file, key)
    else:
        pass


def input_window(text1):
    text = create_text()
    text.delete('1.0', END)
    text.insert(0.0, text1)


def output_password():
    file = open("mainFile.txt", 'r')
    message = file.read()
    file.close()
    return message


def check_main_password():
    # Main password need for step of security
    main = '7110eda4d09e062aa5e4a390b0a572ac0d2c0220'  # Main save password in sha1
    # default is 1234 (not recommend for use, change it)
    MainCheck1 = (mainPasswordEntry.get()).encode()
    MainCheck2 = hashlib.sha1(MainCheck1)
    if main == MainCheck2.hexdigest():
        return True
    else:
        return False


def backup():  # Backup key and main file on external device
    try:
        shutil.copyfile("mainFile.txt", "E:\BackUp\mainFile.txt")
        shutil.copyfile('crypto.key', 'E:\BackUp\crypto.key')
        input_window("BackUp done successful")
    except:
        input_window("BackUp error")


#  Tkinter
def login():
    global entryLogin
    labelLogin = Label(text="Login-", font='arial 15')
    labelLogin.place(x=40, y=0)
    entryLogin = Entry(bd=3, width=40)
    entryLogin.place(x=100, y=4)


def password():
    global entryPassword
    labelPassword = Label(text="Password-", font='arial 15')
    labelPassword.place(x=0, y=28)
    entryPassword = Entry(bd=3, width=40)
    entryPassword.place(x=100, y=33)


def main_password():
    global mainPasswordEntry
    mainPasswordLabel = Label(text="MainPassword-", font='arial 15')
    mainPasswordLabel.place(x=0, y=110)
    mainPasswordEntry = Entry(show='*', bd=3)
    mainPasswordEntry.place(x=150, y=115)


def save_button():
    saveButton = Button(text="Save new Password and Login", command=save, font='arial 11')
    saveButton.place(x=360, y=10)


def create_text():
    global panel
    panel = Text()
    panel.place(x=5, y=150)
    return panel


def backup_button():
    backUp = Button(text="Backup", command=backup)
    backUp.place(x=610, y=0)


def show_button():
    showPass = Button(text='Show Logins and Passwords', command=show, font='arial 10')
    showPass.place(x=300, y=110)


def name():
    global noticeEntry
    noticeLabel = Label(text="Name of Site", font='arial 13')
    noticeLabel.place(x=0, y=59)
    noticeEntry = Entry(bd=3, width=40)
    noticeEntry.place(x=100, y=60)


def edit_button():
    editButton = Button(text="Save edit", command=edit)
    editButton.place(x=590, y=120)


def edit():
    save = panel.get('1.0', END)
    key = load_key()
    file1 = 'mainFile.txt'  # File with data
    try:
        decrypt(file1, key)
    except:  # if no file, create it
        file = open('mainFile.txt', 'w')
        file.close()
    # Create variable with data from input
    file = open('mainFile.txt', 'w')
    file.write(save)
    file.close()
    encrypt(file1, key)
    input_window("Edit done successful")


root = Tk()  # Create window
root.title("Safe")
root.geometry("660x550")
root.resizable(width=False, height=False)
login()
password()
main_password()
save_button()
create_text()
backup_button()
show_button()
name()
edit_button()
root.mainloop()
