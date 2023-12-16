from SendPage import SendEmail
from ReceivePage import ViewEmail
from manageInfo import ManangeUserInfo
from LibraryAndUtils import *
import threading
import time

class MainMenu:
    def __init__(self):
        self.stop_thread = False
        self.config = ManangeUserInfo.load_config()
        while True:
            self.menu()
            self.time_counter_thread = threading.Thread(target=self.run_time_counter_to_download)
            self.time_counter_thread.start()

    def menu(self):
        clear_screen()
        print("MENU")
        print("1. SEND EMAIL")
        print("2. VIEW MAIL")
        print("3. EXIT")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            SendEmail()
        elif choice == "2":
            email_view = ViewEmail()
            email_view.download_tab()
            email_view.run_received_tab()
        elif choice == "3":
            print("Exiting...")
            self.press_exit()
            exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    def press_exit(self):
        self.stop_thread = True
        ManangeUserInfo.delete_config_file()

    def run_time_counter_to_download(self):
        counter = 0
        while True:
            time.sleep(1)
            counter += 1
            if not self.stop_thread and counter % int(self.config['AUTOLOAD']) == 0:
                email_view = ViewEmail()
                email_view.download_tab()
            elif self.stop_thread:
                ManangeUserInfo.delete_config_file()
                break
