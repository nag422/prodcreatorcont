from django.core.mail import EmailMessage
from django.contrib.auth.models import User

import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()






class MassMail:
    @staticmethod
    def send_emails(adminmessage, data):

        connection = mail.get_connection()
        # Manually open the connection
        connection.open()

        # Construct an email message that uses the connection
        mailrecipientlist = []
        for every in data:
            # Construct two more messages
            composingemail = EmailMessage(
            subject='ContentBond - info', body=adminmessage, to=[User.objects.get(pk=int(every['user_ptr_id'])).email])
            mailrecipientlist.append(composingemail)
           

        # Send the two emails in a single call -
        connection.send_messages(mailrecipientlist)
        # The connection was already open so send_messages() doesn't close it.
        # We need to manually close the connection.
        connection.close()