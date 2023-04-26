from django.core.mail import EmailMessage

senderEmail = "organisenea@gmail.com"

def sendEmail(subject, body, to):

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=senderEmail,
        to=[to],
        bcc=[],
        reply_to=[senderEmail],
        headers={"Message-ID": "foo"},
    )

    email.send()