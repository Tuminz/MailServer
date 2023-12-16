from Library import *
from Menu import MainMenu

class Login:
    def __init__(self):
        self.input_username = None
        self.input_email = None
        self.input_password = None
        self.input_server = None
        self.input_SMTP_PORT = None
        self.input_POP3_PORT = None
        self.auto_load = "10" 

    def connect_to_smtp_server(self):
        try:
            with socket.create_connection((self.input_server, int(self.input_SMTP_PORT))) as server_socket:
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

    def connect_to_pop3_server(self):
        try:
            with socket.create_connection((self.input_server, int(self.input_POP3_PORT))) as server_socket:
                server_socket.send('CAPA\r\n'.encode())
                server_socket.send(f'USER {self.input_email}\r\n'.encode())
                server_socket.send(f'PASS {self.input_password}\r\n'.encode())
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

    def check_connection(self):
        print("Waiting for connection...")
        if self.connect_to_smtp_server() and self.connect_to_pop3_server():
            self.save_config()
            print("Connected successfully.")
            print("Configuration saved successfully.")
            time.sleep(1)
            MainMenu()

    def save_config(self):
        config = {
            "NAME": self.input_username.strip(),
            "EMAIL": self.input_email.strip(),
            "PASSWORD": self.input_password.strip(),
            "SERVER": self.input_server.strip(),
            "SMTP_PORT": self.input_SMTP_PORT.strip(),
            "POP3_PORT": self.input_POP3_PORT.strip(),
            "AUTOLOAD": self.auto_load
        }
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file)


    def login_menu(self):
        print("LOGIN")
        print("1. Enter your information")
        print("2. Exit")

        while True:
            choice = input("Enter your choice (1-2): ")
            if choice == "1":
                clear_screen()
                self.input_username = input("Enter your username: ")
                self.input_email = input_and_check_valid_email_address("Enter your email: ")
                self.input_password = input("Enter your password: ")
                self.input_server = input("Enter your server: ")

                while True:
                    self.input_SMTP_PORT = input("Enter your SMTP port: ")
                    if self.input_SMTP_PORT.isdigit():
                        break 
                    else: 
                        print("Invalid SMTP port. Please enter an integer.")

                while True:
                    self.input_POP3_PORT = input("Enter your POP3 port: ")

                    if self.input_POP3_PORT.isdigit():
                        break
                    else:
                        print("Invalid POP3 port. Please enter an integer.")

                self.check_connection()
            elif choice == "2":
                print("Exiting...")
                exit()
            else:
                print("Invalid choice. Please enter a number between 1 and 2.")