
import smtplib
from email.mime.text import MIMEText

from budgie.configuration import settings


class SMTPConfigurationError(Exception):
    pass


class SMTPClient(object):
    """
    The SMTP client to send email when any incident is detected.

    """

    def __init__(self, startls=False, auth=False):
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
            if not (self.smtp_config.get('username') and self.smtp_config.get('password')):
                raise SMTPConfigurationError('Please provide a `smpt.username` and `smtp.password` in config file.')

            self.smtp_server.login(self.smtp_config.username, self.smtp_config.password)

        return self

    def send(self, from_, to, subject, body, cc=None, bcc=None):
        """

        :param from_: From address
        :param to: Target address
        :param subject: E-mail subject.
        :param body: The email body in plain/unicode text.
        :param cc:
        :param bcc:
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
