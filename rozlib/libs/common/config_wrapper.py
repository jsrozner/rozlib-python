from __future__ import annotations

import logging
from dataclasses import dataclass, fields
import pprint

# effectively wraps a module singleton
"""
Note that we needed a config wrapper so that we could call get_config() once in other modules, like
`c = get_config()`
At the point where get_config() is called, we need to return an already initialized class. 
So we return the wrapper. 

Then when we dereference c.<some field>, we use some getattr magic to deref the 
config object that is wrapped by configwrapper.
"""
class _ConfigWrapper:
    def __init__(self):
        # module singleton
        self.config = None

    def set_config(self, c):
        logging.info(f"Setting config to \n{pprint.pformat(c)}")
        if self.config is not None:
            raise Exception("Config has already ben set once")
        self.config = c

    def __getattr__(self, name):
        # global __config
        if self.config is None:
            raise Exception("Config has not been set")
        return getattr(self.config, name)

    # def __getattribute__(self, name):
    #     """Ensure we catch all attribute access."""
    #     if name == "__getattr__" or name == "__getattribute__":
    #         return object.__getattribute__(self, name)
    #     return self.__getattr__(name)


__cwrapper = _ConfigWrapper()


@dataclass
class Config:
    """
    Use this class as a module singleton, e.g.

    # define get_config method
    import _config
    def get_config():
        return __config

    # define config subclass
    class ConfigSubClass(Config):
        # define fields

    ####
    # from main module
    myconfig = ConfigSubClass(
        # config values
    )
    set_config(myconfig)

    ###
    # from another submodule
    import get_config
    c = get_config()

    """
    pass

def set_config(c: Config):
    __cwrapper.set_config(c)

    # global __config
    # print("setting config")
    # if __config is not None:
    #     raise Exception("Config has already ben set once")
    # __config = c
    # print(__config)

# Should be used only once
# Another config module (or main program) should define a new get_config() function with correct
# typing signature
#
# ` def get_config() -> ConfigSubclass:
#       return _config()
# `
def _config():
    return __cwrapper

