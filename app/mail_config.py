from flask_mail import Mail

mail = Mail()

def init_mail(app):
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='hackerbytez128@gmail.com',
        MAIL_PASSWORD='xdvyehgkuegulitx'
    )

    mail.init_app(app)
    