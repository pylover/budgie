#! /usr/bin/env python3

import sys
import io
import pickle
import base64


if __name__ == '__main__':

    buffer = io.BytesIO()

    data = {
        'cpu': 40,
        'memory': 50
    }

    # Dumping
    pickle.dump(data, buffer)

    # Encrypting
    # TODO: encrypt data using pycrypto, not required, because the connection is made by SSH.

    # Encode the binary as base64
    buffer.seek(0)
    base64.encode(buffer, sys.stdout.buffer)
