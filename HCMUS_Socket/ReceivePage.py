from LibraryAndUtils import *
from MailReceiver import EmailShow, EmailGetter, EmailManager, EmailDownloader, EmailFilter
from ManageInfo import ManangeUserInfo

class ViewEmail:
    def __init__(self):
        self.email_list = []
        self.root = None

    def path_to_sub_folder(self, folder_name):
        config = ManangeUserInfo.load_config()
        path = os.path.join(f"{SAVE_FOLDER}_{config['EMAIL']}", folder_name)
        return path

    def get_email(self, folder_path, file_name):
        response = b""
        path_file = os.path.join(folder_path, file_name)

        with open(path_file, 'rb') as file:
            response = file.read()
        
        return response, EmailGetter.get_sender(response.decode(FORMAT)), \
            EmailGetter.get_subject_email(response.decode(FORMAT)),\
            EmailGetter.get_email_content(response.decode(FORMAT))
    
    def save_attachments(self, response, email_id, folder, new_win):
        config = ManangeUserInfo.load_config()
        mail_folder = os.path.join(f"{SAVE_FOLDER}_{config['EMAIL']}", folder)
        mail_path = os.path.join(mail_folder, f"{email_id} attachment")
        os.makedirs(mail_path, exist_ok=True)

        attachment_pattern = re.compile(rb'Content-Disposition:.*?attachment; filename="(.*?)"', re.DOTALL)
        attachments = re.finditer(attachment_pattern, response)

        for match in attachments:
            attachment_filename = match.group(1).decode(FORMAT)
            attachment_path = os.path.join(mail_path, f"{attachment_filename}")

            attachment_start = response.find(b'\r\n\r\n', match.end()) + 4
            attachment_end = response.find(b'\r\n\r\n', attachment_start)
            
            with open(attachment_path, 'wb') as attachment_file:
                attachment_data = response[attachment_start:attachment_end]
                encoded_data = base64.b64decode(attachment_data)
                attachment_file.write(encoded_data)
   
    def show_mail(self, response, sender, subject, content, email_id, folder):
        EmailManager.update_status_of_mail(email_id, self.email_list)

        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Content: \n{content}")

        if NOTICE.encode() in response:
            save_attach_choice = input("Save attachments? (yes/no): ").strip().lower()
            if save_attach_choice == "yes":
                self.save_attachments(response, email_id, folder, None)

        selected_item = input("Press Enter to return to the main menu.")
        self.email_list = EmailShow.show_download_mail()
    
    def download_tab(self):
        EmailFilter.create_filter_folder()
        EmailDownloader.download_emails_pop3()

    def run_received_tab(self):
        self.email_list = EmailShow.show_download_mail()

        print("Folders:")
        for folder in FOLDER_LIST:
            print(folder)

        folder_name = input("Enter folder name to view emails (press Enter to exit): ").strip()
        if folder_name == "":
            return

        if folder_name.upper() not in FOLDER_LIST:
            print("Invalid folder name.")
            return

        for email in self.email_list:
            if email['folder'] == folder_name:
                print(f"{email['sender']}, {email['mes_id']}, {email['status']}")       

        email_id = input("Enter the ID of the email to view (press Enter to exit): ").strip()
        if email_id == "":
            return
        
        for email in self.email_list:

            if email['mes_id'] == email_id and email['folder'] == folder_name:
                folder_path = self.path_to_sub_folder(folder_name)
                file_name = f"{email['sender']}, {email['mes_id']}"
                response, sender, subject, content = self.get_email(folder_path, file_name)
                self.show_mail(response, sender, subject, content, email_id, folder_name)
                break
        else:
            print("Email not found.")

if __name__ == "__main__":
    email_view = ViewEmail()
    email_view.run_received_tab()