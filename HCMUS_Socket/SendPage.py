from InterfaceLib import *
from MailSender import EmailClient_Send
from MailLib import os

import keyboard
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#---- SEND TAB
class SendTab:
    def __init__(self):
        self.filename_list = []
        #self.to_tab()
        self.send_tab = None

    def open(self):
        root = Tk()
        root.withdraw()
        #@ can change to open more files
        filename = askopenfilename()
        
        if filename:
            file_size = os.path.getsize(filename) / (1024**2)
            if file_size <= 3:
                print(filename)
                self.filename_list.append(filename + '  ')
                self.update_label_to()

    def update_label_to(self):
        filenames = ''.join(self.filename_list)
        max_display_length = 115
        filenames_with_newlines = '\n'.join([filenames[i:i + max_display_length] for i in range(0, len(filenames), max_display_length)])
        #self.my_label_attached_file.config(text=filenames_with_newlines)

    def to_tab(self):
        clear_screen()
        print("To input more than one address, please use comma to separate!")
        to = input("TO: ").strip()
        cc = input("CC: ").strip()
        bcc = input("BCC: ").strip()
        subject = input("SUBJECT: ")
        print("CONTENT<Use Ctrl + Z --> Enter to stop writing>: ")
        content = sys.stdin.read()

        choice = input("ATTACH NEW FILES<Type 1 to attach new files or enter to ignore>: ")

        if choice == "1":
            self.open()
            #root = Tk()
            #root.withdraw()
            #attached_files = askopenfilenames(multiple=True)
            #print("ATTACHED FILES:")
            #for file in attached_files:
            #    print(file)

        #clear_screen()
        #print("**VERIFY YOUR EMAIL**")
        #print("TO:")
        #for addr in to:
        #    print(addr)
        #print("CC:", cc)
        #for addr in cc:
        #    print(addr)
        #print("BCC:", bcc)
        #for addr in bcc:
        #    print(addr)
        #print("SUBJECT:", subject)
        #print("CONTENT:")
        #print(content)
        #print("ATTACHED FILES:")
        #for file in attached_files:
        #    print(file)

        print("")
        print("Press 1 to send email.")
        print("Press 2 to compose again.")
        print("Press 3 to send and compose another email.")
        print("Press ESC to back to the main screen.")

        key = keyboard.read_key()
        if key == "1":
            print("Sending email...")
            EmailClient_Send.run_send_mail_program(to, cc, bcc, subject, content, self.filename_list)
            input("Press any key to back to main menu...")
        if key == "2":
            self.menu()
        if key == "3":
            EmailClient_Send.run_send_mail_program(to, cc, bcc, subject, content, self.filename_list)
            self.menu()
        if key == "4":
            self.press_exit()



