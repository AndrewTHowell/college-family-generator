import smtplib

from email.message import EmailMessage


class Emailer():

    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)

        self.fromAddress = "howelldrew99@gmail.com"

        # Next, log in to the server
        self.server.starttls()
        self.server.login(self.fromAddress, "mpnlqxibgjepgkbf")

    def send(self, toAddress, subject, body):
        self.msg = EmailMessage()

        self.msg['From'] = self.fromAddress
        self.msg['To'] = toAddress
        self.msg['Subject'] = subject

        self.msg.set_content(body)

        self.server.send_message(self.msg)

# emailer = Emailer()
# emailer.send()
