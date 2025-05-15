import smtplib
from email.message import EmailMessage

def send_email_report(subject, body, recipient, smtp_user, smtp_pass, smtp_server='smtp.gmail.com', port=587):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = recipient

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        print(f"[+] Email sent to {recipient}")
