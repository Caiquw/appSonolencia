from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition
)
from config import SENDGRID_CONFIG
from datetime import date
import base64

def enviar_relatorio(arquivo_html):
    with open(arquivo_html, "rb") as f:
        conteudo = base64.b64encode(f.read()).decode()

    mensagem = Mail(
        from_email   = SENDGRID_CONFIG["remetente"],
        to_emails    = SENDGRID_CONFIG["supervisor"],
        subject      = f"Relatório Sonolência — {date.today().strftime('%d/%m/%Y')}",
        html_content = "<p>Segue em anexo o relatório diário de sonolência.</p>"
    )

    anexo = Attachment(
        file_content = FileContent(conteudo),
        file_name    = FileName("relatorio.html"),
        file_type    = FileType("text/html"),
        disposition  = Disposition("attachment")
    )
    mensagem.attachment = anexo

    try:
        sg = SendGridAPIClient(SENDGRID_CONFIG["api_key"])
        response = sg.send(mensagem)
        print(f"Status code: {response.status_code}")
        print(f"Headers: {response.headers}")  # adiciona isso

    except Exception as e:
        print(f"✘ Erro: {e}")