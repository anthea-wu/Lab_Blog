from flask import current_app, render_template
from threading import Thread
from flask_mail import Message
from app_blog import mail

def send_mail(sender, recipients, subject, template, mailtype='html', **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, sender=sender, recipients=recipients)

    if mailtype=='html':
        msg.html = render_template(template+'.html', **kwargs)
    elif mailtype=='txt':
        msg.body = render_template(template+'.txt', **kwargs)
    elif mailtype=='body':
        msg.body = template

    thr = Thread(target=send_async_email, args=[app,msg])
    thr.start()

    return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)