import os
import smtplib
import json
from email.message import EmailMessage
from email.headerregistry import Address
import logging

logging.basicConfig(level=logging.INFO, 
                    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S')

class Newsletter():
  
    def __init__(self):
        self.smtp_port = 587 # Default
        self.smtp_server = ""
        self.html_code = """\
        <html>
        <body>      """
        self.images = []
        self.subject = "Newsletters"


    def initialise_email_sender(self, smtp_username, smtp_password, smtp_email_adress=None):
        """
        This function initialises the email sender
        
        :param smtp_username: The username of the email account you want to send emails
        from
        :param smtp_password: The password for the email account you want to send emails
        from
        :param smtp_email_adress: The email address you want to send the emails from. If
        you don't specify this, it will default to the username you specified
        """
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_email_adress = smtp_email_adress
        logging.info("Set email sender: "+ str(self.smtp_email_adress))


    def find_smtp_server(self, path_to_server_list="server_list.json"):
        """
        Given an email address, find the email server that the email address is
        associated with
        
        :param path_to_server_list: the path to the server list file
        """
        email_domain = self.smtp_email_adress.split('@')[-1]
        # maybe use a dict to save the server list such that
        # gmail: {gmail.com, gmail.fr, etc}
        server_list_file = open(path_to_server_list)
        server_list = json.load(server_list_file)
        self.smtp_server = server_list[email_domain][0]
        self.smtp_port = int(server_list[email_domain][1])
        logging.info("SMTP Serveur: " + str(self.smtp_server))
        logging.info("SMTP Port: " +str(self.smtp_port))
        server_list_file.close()

    def set_smtp_server(self, smtp_server):
        self.smtp_server = smtp_server

    def set_smtp_server(self, smtp_port):
        self.smtp_port = smtp_port

        
    def add_receiver(self, receivers):
        list_receivers = receivers.split(',')
        adress_receivers = []
        for receiver in list_receivers:
            username_receiver, domain_receiver = receiver.split('@')
            adress_receivers.append(Address(display_name=username_receiver.strip(), username=username_receiver.strip(), domain=domain_receiver.strip()))
        self.receivers = adress_receivers
        print(self.receivers)

    def set_subject(self, subject):
        self.subject = subject

    def set_images(self, path_to_images):
        self.images = path_to_images

    def set_html(self, html_code): 
        self.html_code = html_code


    def write_email(self):
        self.msg = EmailMessage()
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.smtp_email_adress
        self.msg['To'] = self.receivers
        figure_id = []
        for number_of_image in range(len(self.images)):
            figure_id_k = 'image'+str(number_of_image+1)
            figure_id += [figure_id_k]
            self.html_code += """<img src="cid:{figure_id_1}" />""".format(figure_id_1=figure_id_k)

        self.html_code += """</body>
        </html>"""
        self.msg.add_alternative(self.html_code, subtype='html')
        for k, image_path in enumerate(self.images):
            with open(image_path, 'rb') as img:
                
                self.msg.get_payload()[0].add_related(img.read(), 'image', 'png', cid=figure_id[k])
  

    def send_email(self):
      self.write_email()
      with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
          server.starttls()
          server.login(self.smtp_username, self.smtp_password)
          server.sendmail(self.smtp_email_adress, self.msg['To'], self.msg.as_string())
          logging.info("Email sent")


if __name__=="__main__":
    news = Newsletter()
    news.initialise_email_sender('username','password',smtp_email_adress='example@example.com')
    news.add_receiver('example@example.com')
    news.write_email()