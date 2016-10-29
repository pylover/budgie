#! /usr/bin/env python3

import sys
import io
import subprocess
import pickle
import base64


def write_output(data):
    buffer = io.BytesIO()

    # Dumping
    pickle.dump(data, buffer)

    # Encryption
    # NOTE: encrypt data using pycrypto, not required, because this shell is behind the SSH.

    # Encode the binary as base64
    buffer.seek(0)
    base64.encode(buffer, sys.stdout.buffer)


def execute_subprocess(command):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()
    if stderr and stderr.strip():
        raise subprocess.SubprocessError('The command: "%s" failed\n%s' % (
            command,
            stderr.decode()
        ))

    return stdout.decode().strip()


def get_cpu_usage():
    return float(
        execute_subprocess("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'")
    )


def get_memory_usage():
    return float(
        execute_subprocess("free | grep Mem | awk '{print $3/$2 * 100.0}'")
    )


def main():

    data = {
        'cpu': get_cpu_usage(),
        'memory': get_memory_usage()
    }

    write_output(data)
    return 0


if __name__ == '__main__':
    sys.exit(main())

