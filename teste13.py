from Drivers.Email_Drivers.smtp import SMTPClient


client = SMTPClient(username='breno19091998@gmail.com', password='dngs rsbe btfj rdqt', 
                    server='gmail')
client.enviar_email(
    to='breno19091998@hotmail.com',
    subject='Teste de E-mail',
    body='Olá, este é um e-mail de teste.'
    attachments=['/caminho/para/anexo1.pdf', '/caminho/para/anexo2.jpg']
)

print('Email enviado com sucesso')