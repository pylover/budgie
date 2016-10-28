

import pymlconf


__builtin_configurations = """

workers: 10

db:
  uri: sqlite:///%(here)s/../data/devdata.db
  echo: true

clients:
  localhost:
    address: 127.0.0.1
    port: 22
    username: vahid
    auth: password-less
    alerts:
      -
        type: memory
        limit: 50%%
      -
        type: cpu
        limit: 20%%

"""


# This is proxy to the main configuration instance, It allows the other modules to import the `settings` from this
# module, before it get loaded.
settings = pymlconf.DeferredConfigManager()


def init(config_file=None):
    settings.load(init_value=__builtin_configurations, files=config_file)



