#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

## Standard Libraries
from pprint import pformat
from pprint import pprint
import json
import pickle
import hashlib

"""
 BaseObject provides a template of useful methods for all classes to inherit
"""
class BaseObject(object):

    def __init__(self, state=None):
        self.isValid = False

        if state is None:
            self.tracking_state = False
        else:
            if isinstance(state, State):
                self.tracking_state = True
                self.pg_state = state
            else:
                raise TypeError("state argument was not instance of <State>")

    def meta(self):
        return list(self.__dict__.keys())

    def ready(self, throw=False):
        if throw == True:
            if self.isValid != True:
                raise ValueError("Unable to successfully instantiate object of class::"+self.__class__.__name__)
        else:
            return self.isValid

    def serialize(self):
        try:
            return pickle.dumps(self.__dict__)
        except Exception as e:
            return {'serialize_error': e}

    def marshall(self):
        try:
            return json.dumps(self.__dict__)
        except TypeError as e:
            return {'marshall_error': e}

    def dump(self):
        try:
            j = self.marshall()
            p = self.serialize()
            pd = hashlib.sha1(p).hexdigest()
            jd = hashlib.sha1(p).hexdigest()
            return {
                "json": j,
                "json_digest": jd,
                "json_digest_method": "SHA1",
                "pickle": p,
                "pickle_digest": pd,
                "pickle_digest_method": "SHA1"
            }
        except:
            raise

    def getProp(self, prop=None):
        if prop not in self.meta():
            raise ValueError(str(prop)+" is not a valid property to get()")
        else:
            return getattr(self, prop)

    def getParam(self, param=None):
        return self.getProp(param)

"""
 Borg provides a way to implement trivial Singletons, rather then sharing an
 object the borg provides any number of objects with the same internal data
"""
class Borg(BaseObject):
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state

"""
 This class is designed to store the program state in a fashion to be used via
 multiple modules and provides a singleton-like way to access the state of the program
"""
class State(Borg):
    def __init__(self):
        Borg.__init__(self)
        self.isValid = True
        self.ready(throw=True)

def main():
    pass

if __name__=="__main__":
    main()
