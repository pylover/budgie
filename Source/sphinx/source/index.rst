
.. budgie documentation master file, created by
   sphinx-quickstart on Mon Jul 20 22:05:40 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. DOC TODO:
   - Document about customizing the attachment by inheriting


Budgie
======


- How can send an ssh command on windows? cygwin, or new ssh
  implementation from microsoft? at all, I assume all workstations are
  linux.

- Observation processes must be asynchronous. for example 20 workers
  will waiting for client's result at the same time, simultaneously.

- Because we are going to save the encryption key on the clients machine
  and everyone can access them, we should use asymmetric encryption.
  but at all, i cannot understand if, the connection is made by ssh between
  the client & server, why data encryption was requested?
  So I'll ignore the encryption phase, because I believe the all exchanged data between server & client is hardly
  encrypted using 4096 bits ssh key.

- The database object will be created using ORM in code-first manner.

- For the configuration I prefer to use ``YAML`` instead of the ``XML``. it's
  so clear and readable. so my own open-source configuration
  library will be used.

- If time available in the future. the PSExec and or winexec will be
  tested for windows clients. A few years ago, I was used them for an
  ITIL(Help-Desk) project, to executing a command on the remote machine
  using Win-IPC, as the file & printer sharing is working. But it's very
  un-secure.

- Using github's kanban, to manage project.


Limitations
-----------


- Only works with linux

- Require Python3.5 or higher

- Does not encrypting data from client script, because the data will be
  sent over the SSH


Dependencies
------------

The main dependencies of the project is listed below:

- https://github.com/pylover/pymlconf
- http://sqlalchemy.org/
- https://github.com/paramiko/paramiko

Requirements for running tests:

- https://github.com/carletes/mock-ssh-server
- http://nose.readthedocs.io/en/latest/

Requirements for building documents:

- sphinx
- texlive-latex-base
- texlive-latex-recommended
- texlive-latex-extra
- texlive-fonts-recommended

API
---

.. toctree::
   :maxdepth: 4

   api



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

