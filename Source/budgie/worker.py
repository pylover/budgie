
import time
from datetime import datetime
from os.path import exists
import pickle
import base64
import threading

import paramiko

from budgie.configuration import settings
from budgie.models import AgentLog, DBSession


class HelpDeskWorker(threading.Thread):
    result = None
    error = None
    sleep_time = 0.01

    def __init__(self, username, host, port=22, key_file=None, password=None, agent_script=None):
        """
        This object is responsible for dispatching the agent on the client, run it and return the result provided by
        the agent.

        :param username: The ssh username to connect to the target host.
        :param host: The hostname to connect.
        :param port: the ssh port, default: 22.
        :param key_file: The private ssh key file to connect in password-less manner.
        :param password: The ssh password.
        :param agent_script: The full path to the agent script.


        .. none:: One of ``password`` and or ``key_file`` have to be used.

        """
        
        super(HelpDeskWorker, self).__init__(daemon=True, name='%s@%s' % (username, host))

        # Checking the agent script
        agent_script = agent_script or settings.agent.filename
        if not exists(agent_script):
            FileNotFoundError('The file: %s was not found' % agent_script)

        if not (password or key_file):
            raise ValueError('One of the `password` and or `key_file` must be passed.')

        self.username = username
        self.host = host
        self.port = port
        self.key_file = key_file
        self.password = password
        self.agent_script = agent_script

    def run(self):
        new_log = AgentLog(
            hostname=self.host,
            entry_time=datetime.now()
        )

        try:
            self.store_and_execute_aget()

            if self.error is not None:
                new_log.error = self.error

            new_log.cpu = self.result.get('cpu')
            new_log.memory = self.result.get('memory')
        finally:
            new_log.end_time = datetime.now()

        DBSession.add(new_log)
        DBSession.commit()

    def store_and_execute_aget(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.key_file is not None:
            with open(self.key_file) as key_file_object:
                user_key = paramiko.RSAKey.from_private_key(key_file_object)
        else:
            user_key = None

        client.connect(
            self.host,
            port=self.port,
            username=self.username,
            pkey=user_key,
            password=self.password
        )
        try:

            # Putting the agent script on the target host.
            sftp_client = client.open_sftp()
            sftp_client.put(self.agent_script, 'budgie_agent.py')
            sftp_client.close()

            # Making the target script executable
            client.exec_command('chmod +x budgie_agent.py')

            stdout, stderr = b'', b''
            ssh_transport = client.get_transport()
            channel = ssh_transport.open_session()
            # chan.settimeout(3 * 60 * 60) # TODO: What is this?
            channel.setblocking(0)
            channel.exec_command('./budgie_agent.py')

            while True:  # monitoring process
                # Reading from output streams
                while channel.recv_ready():
                    stdout += channel.recv(1000)
                while channel.recv_stderr_ready():
                    stderr += channel.recv_stderr(1000)
                if channel.exit_status_ready():  # If completed
                    break
                time.sleep(self.sleep_time)

            exit_code = channel.recv_exit_status()
            ssh_transport.close()

            if exit_code != 0:
                self.error = stderr
            else:
                pickled_data = base64.decodebytes(stdout)
                self.result = pickle.loads(pickled_data)

        finally:
            client.close()



