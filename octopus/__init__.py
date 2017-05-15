__version__ = '0.1.0-dev'

import inspect
from configparser import ConfigParser

config = ConfigParser()
config.read('conf/octopus.conf')

__all__ = sorted(name for name, obj in locals().items()
                 if not (name.startswith('_') or inspect.ismodule(obj)))

del inspect
