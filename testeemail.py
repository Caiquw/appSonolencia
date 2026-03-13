from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Cole os valores diretamente aqui para descartar erro no config.py
API_KEY    = "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"  # sua chave
REMETENTE  = "castro.caique@outlook.com"
DESTINATARIO = "appsonolenciaunaerp@outlook.com"

mensagem = Mail(
    from_email   = REMETENTE,
    to_emails    = DESTINATARIO,
    subject      = "Teste SendGrid",
    html_content = "<p>Teste de envio</p>"
)

try:
    sg = SendGridAPIClient(API_KEY)
    response = sg.send(mensagem)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.body}")
    print(f"Headers: {response.headers}")
except Exception as e:
    print(f"Erro completo: {e}")