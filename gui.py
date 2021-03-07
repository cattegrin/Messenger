from twilio.rest import Client
from tkinter import *
from tkinter.messagebox import showinfo
import xlrd
import smtplib
from email.message import EmailMessage

# Parameter Values
VERSION = 1.0
sid = 'AC1a8ebc3aa32bf1ed04d4b078b3f99075'
token_file = open('token.txt', 'r')
TOKEN = token_file.read()
token_file.close()
##########################################
client = Client(sid, TOKEN)                                             # Creates Twilio client connection


# Class to hold data for each person
class Person:
    def __init__(self, n, phone, email):
        self.name = n                                   # Member name
        self.phone = phone                              # Cell Number
        self.email = email                              # Email Address
        self.status = BooleanVar()                          # Int to hold status
        self.status.set(False)


# Main Application Class
class Messenger(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root                                                # Sets application root window
        self.msg = ""                                                   # Inits message to empty

        self.intro = BooleanVar()
        self.intro.set(False)                                             # Inits intro boolean to False

        self.sig = ""                                                   # Inits signature to empty

        self.texts = BooleanVar()
        self.texts.set(False)                                              # Inits text messages to false

        self.emails = BooleanVar()
        self.emails.set(False)                                          # inits emails to false

        self.vsb = Scrollbar(self.root, orient="vertical")              # Init scroll bars and text boxes
        self.text = Text(self.root, width=25, height=40,
                         yscrollcommand=self.vsb.set)
        self.vsb2 = Scrollbar(self.root, orient="vertical")
        self.text2 = Text(self.root, width=25, height=40,
                          yscrollcommand=self.vsb2.set)

        self.build()                                                    # Builds Text Boxes

        self.items = [self.buttons(), self.checks(), self.entries(),
                      self.show_people()]                               # Displays items on screen

    # Sends message to Fraters
    def send_message(self):  # builds and sends messages
        message = self.items[2][1].get()                            # Gets message from entry box
        people = self.items[3][0] + self.items[3][1]                # Gets both people lists

        sig = self.items[2][3].get()                                # Gets signature from entry box
        if sig != "":                                          # if signature not empty, attach
            message += "\n\n" + self.sig

        if self.texts.get():                                                # If sending a text
            for p in people:                                          # loops through all people
                if p.status.get():                                    # Person is on message roster
                    if self.intro.get():
                        client.messages.create(to=p.phone, from_="14159095746",
                                               body="Hey " + p.name + ",\n\n" + message)
                    else:
                        client.messages.create(to=p.phone, from_="14159095746",
                                               body=message)

            showinfo("Texts Sent", "Text broadcast completed successfully")

        if self.emails.get():                     # if sending emails
            user_email = "tkeupcry@gmail.com"               # sending emails from (Cryso Gmail account)
            pass_file = open("gmail_password.txt", "r")     # gets account password from file
            PW = pass_file.read()
            pass_file.close()

            msg = EmailMessage()                            # Creates email message
            msg.set_content(message)                        # Sets content of email
            msg['Subject'] = "A message from TKE Upsilon Pi"
            msg['From'] = user_email

            server = smtplib._SSL('smtp.gmail.com', 587)    # Connects to secure SMTP (email) server
            server.login(user_email, PW)                    # Logs us in

            for p in people:                                # loops through all people
                if p.status.get():                          # if contacting this person
                    msg['To'] = p.email                     # sets target email
                    server.send_message(msg)                # sends message


        showinfo("Done!", "Broadcast complete!")

    # Creates all buttons
    def buttons(self):
        #
        send_btn = Button(self.root, text="Send Message",                           # Creates send button
                          bg="green", command=self.send_message, width=15)
        send_btn.grid(column=0, row=0)                                              # Sets button position

        exit_btn = Button(self.root, text="Exit",                                   # Creates exit button
                          bg="red", command=lambda: exit(0), width=15)
        exit_btn.grid(column=0, row=1)                                              # Sets button position

        return[send_btn, exit_btn]                                                  # Returns all buttons

    # Creates default check buttons
    def checks(self):
        # Check buttons: Column 0, row 3+
        intro = BooleanVar()                                               # Include an introduction ("Hey <name>...")?
        intro.set(False)                                                   # default false
        intro_chk = Checkbutton(self.root, text='Include a Greeting',      # Create checkbox
                                var=self.intro)
        intro_chk.grid(row=3, column=0, sticky=W)

        alum = BooleanVar()                                                # Should the builder send messages to Alumni?
        alum.set(False)                                                    # default False
        alum_chk = Checkbutton(self.root, text='Select All Alumni', var=alum,
                               command=lambda: select_all(self.items[3][1]))
        alum_chk.grid(row=4, column=0, sticky=W)

        active = BooleanVar()  # Should the builder send messages to Actives?
        active.set(True)  # default True
        active_chk = Checkbutton(self.root, text='Select All Actives', var=active,
                                 command=lambda: select_all(self.items[3][0]))
        active_chk.grid(row=5, column=0, sticky=W)

        phone_chk = Checkbutton(self.root, text='Send Text Messages', var=self.texts)
        phone_chk.grid(row=6, column=0, sticky=W)

        email_chk = Checkbutton(self.root, text='Send Email Notifications', var=self.emails)
        email_chk.grid(row=7, column=0, sticky=W)

        return [intro_chk, alum_chk, active_chk, phone_chk, email_chk]

    # Creates Labels and Entry Boxes
    def entries(self):
        # Column 1 & 2, Row 0+
        msg_label = Label(self.root, text="Message:  ")  # Creates label
        msg_label.grid(column=1, row=0)  # Adds label
        msg_entry = Entry(self.root, width=80, textvariable=self.msg)  # Creates entry box
        msg_entry.grid(column=2, row=0, columnspan=3)  # Adds entry box

        sig_label = Label(self.root, text="Signature:")
        sig_label.grid(column=1, row=1)
        sig_entry = Entry(self.root, width=80, textvariable=self.sig)
        sig_entry.grid(column=2, row=1, columnspan=3)

        return [msg_label, msg_entry, sig_label, sig_entry]

    # Loads people from Excel
    def load(self, sheet):
        data = []
        for x in range(1, sheet.nrows):  # Loops through rows
            name = sheet.cell(x, 0).value.split(",", 1)                                 # Splits name value
            n = name[1][1:] + " " + name[0]
            data.append(Person(n, sheet.cell(x, 1).value, sheet.cell(x, 2).value))  # Adds person to roster
        return data

    # Adds people to text fields
    def show_people(self):
        roster = xlrd.open_workbook('roster.xls')
        active = roster.sheet_by_index(0)  # Loads Active Roster
        alumni = roster.sheet_by_index(1)  # Loads alumni roster
        act = self.load(active)
        alu = self.load(alumni)

        for a in act:  # Loop through active
            cb = Checkbutton(self.root, text=a.name, variable=a.status, width=25,
                             justify="left")  # Create check button for active
            self.text.window_create("end", window=cb)
            self.text.insert("end", "\n")

        for a in alu:  # Loop through alum
            cb = Checkbutton(self.root, text=a.name, variable=a.status,
                             width=25,  justify="left")  # Create check button for alumni
            self.text2.window_create("end", window=cb)
            self.text2.insert("end", "\n")

        return [act, alu]               # returns person list

    # Creates text boxes to hold people
    def build(self):
        self.vsb.config(command=self.text.yview)
        self.vsb.grid(row=3, rowspan=50, column=3, sticky=NS)
        self.text.config(state="disabled")
        self.text.grid(row=3, rowspan=50, column=2, sticky=W)

        self.vsb2.config(command=self.text2.yview)
        self.vsb2.grid(row=3, rowspan=50, column=5, sticky=NS)
        self.text2.config(state="disabled")
        self.text2.grid(row=3, rowspan=50, column=4, sticky=W)


def select_all(people):                  # Flips states of all given nodes
    for p in people:
        n = p.status
        if n.get():
            n.set(0)
        else:
            n.set(1)


if __name__ == "__main__":
    root = Tk()
    root.title = "Spam The Chapter v" + str(VERSION)
    root.geometry('960x720')
    root.config(bg="gray85")
    Messenger(root)
    root.mainloop()

