

import pymlconf


__builtin_configurations = """

workers: 10

db:
  uri: sqlite:///%(here)s/../data/devdata.db
  echo: true

agent:
  filename: %(here)s/client/budgie_agent.py

clients:


"""


# This is proxy to the main configuration instance, It allows the other modules to import the `settings` from this
# module, before it get loaded.
settings = pymlconf.DeferredConfigManager()


def init(config_file=None, context=None, **kw):
    settings.load(init_value=__builtin_configurations, files=config_file, context=context, **kw)



