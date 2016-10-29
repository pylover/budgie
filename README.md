# budgie
A simple workstation observer across intranet.

### Limitations
 
- Only works with linux
- Require Python3.5 or higher
- Does not encrypting data from client script, because the data will be 
  sent over the SSH

### Install

```bash
    $ cd path/to/Source
    $ pip install -e .
```

### Running tests

```bash
    $ pip install -r requirements.test.txt
    $ nosetests
```

### Command line interface

```bash
    $ budgie -h
    
    usage: budgie [-h] [-c CONFIG_FILE] [-V] {setup-db,run} ...
    
    positional arguments:
    {setup-db,run}        Available commands:
    
    optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG_FILE, --config-file CONFIG_FILE
                        The server configuration file, default:
                        development.yaml
    -V, --version         Show the version.
    

    $ budgie -V
    0.1.0-dev.0
```

### Configuration:

Create a file named 'development.yaml' on the current directory:

```yaml
    workers: 2

    db:
      uri: sqlite:///%(here)s/../data/devdata.db
      # uri: postgresql://scott:tiger@localhost:5432/mydatabase
      # uri: mysql://scott:tiger@localhost/foo
      echo: true

    agent:
      filename: %(root)s/client/budgie_agent.py

    smtp:
      startls: false
      auth: false
      host: localhost
      port: 2526
      local_hostname: localhost

    clients:
      localhost:
        mail: admin@localhost.com
        hostname: localhost
        port: 22
        username: user1
        key_file: path/to/ssh/private/key
        alerts:
          -
            type: memory
            limit: 50
          -
            type: cpu
            limit: 20
```

### Setup database

This command will be create the database objects. set `echo: true` in 
config file to see what is happening.

    $ budgie -c path/to/config/file setup-db
    
### Run 

    $ budgie run
    
    
### Building documents

    $ cd path/to/Source
    $ pip install -r requirements.dev.txt
    
    $ cd path/to/Source/sphinx/source
    $ sudo apt install texlive-latex-base texlive-latex-recommended \
         texlive-latex-extra texlive-fonts-recommended
    $ make latexpdf
    $ make html
    