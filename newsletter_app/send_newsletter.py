import os
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import logging

logging.basicConfig(level=logging.INFO, 
                    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S')

class Newsletter():
  
    def __init__(self):
        self.smtp_port = 587 # Default
        self.smtp_server = ""
        self.html_code = """"""
        self.images = []
        self.subject = "Newsletters"


    def initialise_email_sender(self, smtp_username, smtp_password, smtp_email_adress=None):
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_email_adress = smtp_email_adress


    def find_smtp_server(self, path_to_server_list="server_list.json"):
        """
        > Given an email address, find the email server that the email address is
        associated with
        
        :param path_to_server_list: the path to the server list file
        """
        email_domain = self.email_user.split('@')[-1]
        # maybe use a dict to save the server list such that
        # gmail: {gmail.com, gmail.fr, etc}
        server_list_file = open(path_to_server_list)
        server_list = json.load(server_list_file)
        self.smtp_server = server_list[email_domain][0]
        self.smtp_port = server_list[email_domain][1]
        server_list_file.close()

    def set_smtp_server(self, smtp_server):
        self.smtp_server = smtp_server

    def set_smtp_server(self, smtp_port):
        self.smtp_port = smtp_port

        
    def add_receiver(self, receivers):
        self.receivers = receivers

    def set_subject(self, subject):
        self.subject = subject

    def set_images(self, path_to_images):
        self.images = path_to_images

    def set_html(self, html_code): 
        self.html_code = html_code

    def write_email(self):
        self.msg = MIMEMultipart('related')
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.smtp_email_adress
        self.msg['To'] = self.receivers
        self.msg.attach(MIMEText(self.html_code, 'html'))
        for k, image_path in enumerate(self.images):
            self.html_code += '<img src="cid:image'+str(k)+'">'
            with open(image_path, 'rb') as f:
                img_data = f.read()
                img = MIMEImage(img_data)
                img.add_header('Content-ID', '<image'+str(k)+'>')
                self.msg.attach(img)

    def send_email(self):
      self.write_email()
      with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
          server.starttls()
          server.login(self.smtp_username, self.smtp_password)
          server.sendmail(self.smtp_email_adress, self.msg['To'], self.msg.as_string())
          logging.info("email sent")


if __name__=="__main__":
    news = Newsletter()
    news.initialise_email_sender('username','password',smtp_email_adress='example@example.com')
    news.add_receiver('example@example.com')
    news.send_email()