import win32com.client

class outlook():
    def __init__(self):
        self.app = win32com.client.Dispatch("Outlook.Application")

    def enviar_email(self, to, subject, body):
            mail = self.app.CreateItem(0)  
            mail.To = to
            mail.Subject = subject
            mail.Body = body
            mail.Send()


