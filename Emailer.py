import smtplib

from email.message import EmailMessage


class Emailer():

    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)

        fromaddr = "howelldrew99@gmail.com"
        toaddr = "howelldrew99@gmail.com"

        # Next, log in to the server
        self.server.starttls()
        self.server.login(fromaddr, "mpnlqxibgjepgkbf")

        self.msg = EmailMessage()

        self.msg['From'] = fromaddr
        self.msg['To'] = toaddr
        self.msg['Subject'] = "College Family Generator Finished"

        body = "Your College Family Generator has finished."
        self.msg.set_content(body)

    def send(self):
        self.server.send_message(self.msg)


emailer = Emailer()
emailer.send()
