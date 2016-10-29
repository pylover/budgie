
import smtplib
from email.mime.text import MIMEText

from budgie.configuration import settings


class SMTPClient(object):

    def __init__(self, startls=False, auth=True):
        self.smtp_config = settings.smtp
        self.startls = startls or self.smtp_config.startls
        self.auth = auth or self.smtp_config.auth
        self.smtp_server = smtplib.SMTP(
            host=self.smtp_config.host,
            port=self.smtp_config.port,
            local_hostname=self.smtp_config.local_hostname,

        )

    def __enter__(self):
        if self.startls:
            self.smtp_server.starttls()

        if self.auth:
            self.smtp_server.login(self.smtp_config.username, self.smtp_config.password)

        return self

    def send(self, from_, to, subject, body, cc=None, bcc=None):
        """
        Sending messages by email
        """

        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = from_
        msg['To'] = to
        if cc:
            msg['Cc'] = cc
        if bcc:
            msg['Bcc'] = bcc

        self.smtp_server.send_message(msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.smtp_server.quit()
