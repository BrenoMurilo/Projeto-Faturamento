import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from msal import ConfidentialClientApplication

class SMTPClient:

    def __init__(self, username, password, server='office365', port=587):
        self.username = username
        self.password = password
        self.server = server
        self.port = port

    def enviar_email(self, to, subject, body, attachments=None):
        """
        Envia um e-mail com ou sem anexos.

        :param to: Endereço de e-mail do destinatário.
        :param subject: Assunto do e-mail.
        :param body: Corpo do e-mail.
        :param attachments: Lista de caminhos de arquivos para anexar ao e-mail (opcional).
        """
        smtp_server = f'smtp.{self.server}.com'
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Adicionar anexos, se fornecidos
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        attachment = MIMEText(file.read(), 'base64')
                        attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
                        msg.attach(attachment)
                else:
                    print(f"Arquivo não encontrado: {file_path}")

        with smtplib.SMTP(smtp_server, self.port) as server:
            server.starttls()  # Criptografia
            server.login(self.username, self.password)
            server.sendmail(self.username, to, msg.as_string())
