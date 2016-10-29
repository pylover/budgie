
from os.path import abspath, dirname
import pymlconf


BUDGIE_ROOT = abspath(dirname(__file__))


__builtin_configurations = """

workers: 1

db:
  uri: sqlite:///%(here)s/../data/devdata.db
  echo: true

agent:
  filename: %(root)s/client/budgie_agent.py

smtp:
    startls: False
    auth: False
    host: localhost
    port: 25
    local_hostname: localhost
    username:
    password:

clients:


"""


# This is proxy to the main configuration instance, It allows the other modules to import the `settings` from this
# module, before it get loaded.
settings = pymlconf.DeferredConfigManager()


def init(config_file=None, context=None, **kw):
    _context = {
        'root': BUDGIE_ROOT,
        'here': abspath(dirname(config_file)) if config_file else BUDGIE_ROOT
    }

    if context:
        _context.update(context)

    settings.load(init_value=__builtin_configurations, files=config_file, context=_context, **kw)



