from MailLib import json, socket, CONFIG_FILE
from InterfaceLib import *
from Menu import MenuTab

#----- LOGIN TAB
# class LoginTab:
#     def __init__(self):
#         self.root = tb.Window(themename='darkly')
#         self.root.title("MAIL APPLICATION")
#         self.root.geometry(window_size)

#         self.entry_username = None
#         self.entry_email = None
#         self.entry_password = None
#         self.entry_server = None
#         self.entry_SMTP_PORT = None
#         self.entry_POP3_PORT = None
#         self.auto_load = "10" 

#     def check_create_connection_to_server_to_smtp(self):
#         try:
#             with socket.create_connection((self.entry_server.get().strip(), self.entry_SMTP_PORT.get().strip())) as server_socket:
#                 response = server_socket.recv(HEADER).decode()
#                 if not response.startswith('220'):
#                     Messagebox.show_error("Error connecting to server", f"Error: {response}")
#                     return False
#                 else:
#                     Messagebox.show_info("Connect Successfully!!", "SMTP Connection")
#                     server_socket.send("QUIT\r\n".encode()) 
#                     return True
#         except ConnectionRefusedError:
#             Messagebox.show_error("No connection could be made because the target machine actively refused it!", "SMTP Connection Error")
#         except Exception as e:
#             Messagebox.show_error(f"An unexpected error occurred: {e}", "SMTP Error")

#     def check_create_connection_to_server_to_pop3(self):
#         try:
#             with socket.create_connection((self.entry_server.get().strip(), self.entry_POP3_PORT.get().strip())) as server_socket:
#                 server_socket.send('CAPA\r\n'.encode())
#                 server_socket.send(f'USER {self.entry_email.get().strip()}\r\n'.encode())
#                 server_socket.send(f'PASS {self.entry_password.get().strip()}\r\n'.encode())
#                 server_socket.send("QUIT\r\n".encode()) 
#                 response = server_socket.recv(HEADER).decode()
#                 if not response.startswith('+OK'):
#                     Messagebox.show_error("Error connecting to server", f"Error: {response}")
#                     return False
#                 else:
#                     Messagebox.show_info("Connect Successfully!!", "POP3 Connection")
                    
#                     return True
#         except ConnectionRefusedError:
#             Messagebox.show_error("No connection could be made because the target machine actively refused it!", "POP3 Connection Error")
#         except Exception as e:
#             Messagebox.show_error(f"An unexpected error occurred: {e}", "POP3 Error")
    
#     def checker(self):
#         try:
#             smtp = int(self.entry_SMTP_PORT.get().strip())
#             pop3 = int(self.entry_POP3_PORT.get().strip())
#         except ValueError as e:
#             Messagebox.show_error(f"Ports must be integers: {e}", "Connection Error")
#             return

#         if self.check_create_connection_to_server_to_smtp() and self.check_create_connection_to_server_to_pop3():
#             self.save_config()
#             menu_tab = MenuTab(self.root)

#     def save_config(self):
#         config = {
#             "NAME": self.entry_username.get().strip(),
#             "EMAIL": self.entry_email.get().strip(),
#             "PASSWORD": self.entry_password.get().strip(),
#             "SERVER": self.entry_server.get().strip(),
#             "SMTP_PORT": self.entry_SMTP_PORT.get().strip(),
#             "POP3_PORT": self.entry_POP3_PORT.get().strip(),
#             "AUTOLOAD": self.auto_load
#         }
#         with open(CONFIG_FILE, "w") as file:
#             json.dump(config, file)

#     def create_menu_login(self):
#         # Create Frame
#         frame_login = tb.Frame(self.root, bootstyle=f'{color}', width=900, height=500)
#         frame_login.pack(pady=100, padx=50)

#         # Create Label
#         label_login = tb.Label(frame_login, text="LOGIN", bootstyle=f'inverse {color}',
#                             font=(f'{font_interface}', 30, 'bold'))
#         label_login.grid(row=0, column=1, columnspan=3, pady=10)

#         labels = ["USERNAME", "EMAIL", "PASSWORD", "SERVER", "SMTP PORT", "POP3 PORT"]

#         for i, label_text in enumerate(labels, start=1):
#             label = tb.Label(frame_login, text=label_text, bootstyle=f'inverse {color}',
#                             font=(f'{font_interface}', 12))
#             label.grid(row=i, column=0, padx=50, pady=10, sticky="w")

#         # Create Entry

#         self.entry_username = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50)
#         self.entry_username.grid(row=1, column=1, padx=50, pady=10)

#         self.entry_email = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50)
#         self.entry_email.grid(row=2, column=1, padx=50, pady=10)

#         self.entry_password = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50, show='*')
#         self.entry_password.grid(row=3, column=1, padx=50, pady=10)

#         self.entry_server = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50)
#         self.entry_server.grid(row=4, column=1, padx=50, pady=10)

#         self.entry_SMTP_PORT = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50)
#         self.entry_SMTP_PORT.grid(row=5, column=1, padx=50, pady=10)

#         self.entry_POP3_PORT = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50)
#         self.entry_POP3_PORT.grid(row=6, column=1, padx=50, pady=10)

#         # Create Button
#         get_info_button = tb.Button(frame_login, bootstyle="light, outline, inverse", 
#                                     text='Submit', padding=10, command=self.checker)
#         get_info_button.grid(row=8, columnspan=3, pady=10, padx=50)

#         self.root.mainloop()


import socket
import json
import time

#CONFIG_FILE = "config.json"
#HEADER = 1024

class LoginTab:
    def __init__(self):
        self.entry_username = None
        self.entry_email = None
        self.entry_password = None
        self.entry_server = None
        self.entry_SMTP_PORT = None
        self.entry_POP3_PORT = None
        self.auto_load = "10" 

    def check_create_connection_to_server_to_smtp(self):
        try:
            with socket.create_connection((self.entry_server, int(self.entry_SMTP_PORT))) as server_socket:
                response = server_socket.recv(HEADER).decode()
                if not response.startswith('220'):
                    print(f"Error connecting to SMTP server: {response}")
                    return False
                else:
                    print("SMTP Connection Successful!!")
                    server_socket.send("QUIT\r\n".encode()) 
                    return True
        except ConnectionRefusedError:
            print("No connection could be made because the target machine actively refused it! (SMTP)")
        except Exception as e:
            print(f"An unexpected error occurred (SMTP): {e}")

    def check_create_connection_to_server_to_pop3(self):
        try:
            with socket.create_connection((self.entry_server, int(self.entry_POP3_PORT))) as server_socket:
                server_socket.send('CAPA\r\n'.encode())
                server_socket.send(f'USER {self.entry_email}\r\n'.encode())
                server_socket.send(f'PASS {self.entry_password}\r\n'.encode())
                server_socket.send("QUIT\r\n".encode()) 
                response = server_socket.recv(HEADER).decode()
                if not response.startswith('+OK'):
                    print(f"Error connecting to POP3 server: {response}")
                    return False
                else:
                    print("POP3 Connection Successful!!")
                    return True
        except ConnectionRefusedError:
            print("No connection could be made because the target machine actively refused it! (POP3)")
        except Exception as e:
            print(f"An unexpected error occurred (POP3): {e}")
   

    def checker(self):
        try:
            smtp = int(self.entry_SMTP_PORT.strip())
            pop3 = int(self.entry_POP3_PORT.strip())
        except ValueError as e:
            #@Messagebox.show_error(f"Ports must be integers: {e}", "Connection Error")
            print("Ports must be integers. Please input again!")
            return

        if self.check_create_connection_to_server_to_smtp() and self.check_create_connection_to_server_to_pop3():
            self.save_config()
            print("Configuration saved successfully.")
            menu_tab = MenuTab()

    def save_config(self):
        config = {
            "NAME": self.entry_username.strip(),
            "EMAIL": self.entry_email.strip(),
            "PASSWORD": self.entry_password.strip(),
            "SERVER": self.entry_server.strip(),
            "SMTP_PORT": self.entry_SMTP_PORT.strip(),
            "POP3_PORT": self.entry_POP3_PORT.strip(),
            "AUTOLOAD": self.auto_load
        }
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file)

    def create_menu_login(self):
        check = False;
        print("LOGIN")
        print("1. Enter your information")
        print("2. Exit")
        
        choice = input("Enter your choice (1-2): ")

        if choice == "1":
            while check == False:
                self.entry_username = input("Enter your username: ")
                self.entry_email = input("Enter your email: ")
                self.entry_password = input("Enter your password: ")
                self.entry_server = input("Enter your server: ")
                self.entry_SMTP_PORT = input("Enter your SMTP port: ")
                self.entry_POP3_PORT = input("Enter your POP3 port: ")
                check = self.checker()
        elif choice == "2":
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 2.")

# if __name__ == "__main__":
#     login_tab = LoginTab()
#     login_tab.create_menu_login()
