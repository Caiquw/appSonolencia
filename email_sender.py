import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import EMAIL_CONFIG
from datetime import date

# Configurações por provedor
PROVEDORES = {
    "gmail": {
        "host": "smtp.gmail.com",
        "porta": 465,
        "ssl": True       # usa SMTP_SSL
    },
    "outlook": {
        "host": "smtp.office365.com",
        "porta": 587,
        "ssl": False      # usa STARTTLS
    }
}

def enviar_relatorio(arquivo_html):
    provedor = EMAIL_CONFIG["provedor"].lower()

    if provedor not in PROVEDORES:
        raise ValueError(f"Provedor '{provedor}' inválido. Use 'gmail' ou 'outlook'.")

    cfg = PROVEDORES[provedor]

    msg = MIMEMultipart()
    msg["From"]    = EMAIL_CONFIG["remetente"]
    msg["To"]      = EMAIL_CONFIG["supervisor"]
    msg["Subject"] = f"Relatório Sonolência — {date.today().strftime('%d/%m/%Y')}"

    msg.attach(MIMEText("Segue em anexo o relatório diário.", "plain"))

    with open(arquivo_html, "rb") as f:
        parte = MIMEBase("application", "octet-stream")
        parte.set_payload(f.read())
    encoders.encode_base64(parte)
    parte.add_header("Content-Disposition", "attachment; filename=relatorio.html")
    msg.attach(parte)

    try:
        if cfg["ssl"]:
            # Gmail — conexão SSL direta
            with smtplib.SMTP_SSL(cfg["host"], cfg["porta"]) as server:
                server.login(EMAIL_CONFIG["remetente"], EMAIL_CONFIG["senha_app"])
                server.sendmail(EMAIL_CONFIG["remetente"], EMAIL_CONFIG["supervisor"], msg.as_string())
        else:
            # Outlook — conexão normal + upgrade para TLS
            with smtplib.SMTP(cfg["host"], cfg["porta"]) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(EMAIL_CONFIG["remetente"], EMAIL_CONFIG["senha_app"])
                server.sendmail(EMAIL_CONFIG["remetente"], EMAIL_CONFIG["supervisor"], msg.as_string())

        print(f"E-mail enviado com sucesso via {provedor.capitalize()}!")

    except smtplib.SMTPAuthenticationError:
        print("Erro de autenticação — verifique e-mail e senha no config.py")
    except smtplib.SMTPException as e:
        print(f"Erro ao enviar e-mail: {e}")