
from MailSender import ClientSendEmail
from Library import os
import keyboard
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#---- SEND TAB
class SendEmail:
    def __init__(self):
        self.attachment_list = []
        self.send_email_screen()
        self.send_tab = None

    def attach_file(self):
        root = Tk()
        root.withdraw()
        filename = askopenfilename()
        
        if filename:
            file_size = os.path.getsize(filename) / (1024**2)
            if file_size <= 3:
                print(filename)
                self.attachment_list.append(filename + '  ')
                self.update_label_to()

    def update_label_to(self):
        filenames = ''.join(self.attachment_list)
        max_display_length = 115
        filenames_with_newlines = '\n'.join([filenames[i:i + max_display_length] for i in range(0, len(filenames), max_display_length)])

    def send_email_screen(self):
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
            self.attach_file()

        print("")
        print("Press 1 to send email.")
        print("Press ESC to back to the main menu.")

        while True:
            key = keyboard.read_key()
            if key == "1":
                print("Sending email...")
                ClientSendEmail.start_sending_process(to, cc, bcc, subject, content, self.attachment_list)
                input("Press any key to back to main menu...")
                break
            elif key == 'esc':
                break



