#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

## Standard Libraries
from pprint import pformat
from pprint import pprint
import json
import jsonpickle
import pickle
import hashlib
import collections

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
    
    def frozen(self):
        try:
            hashable = {}
            for k,v in self.__dict__.items():
                kh = isinstance(k, collections.Hashable)
                vh = isinstance(v, collections.Hashable)
                if kh is True and vh is True:
                    hashable[k] = v
                else:
                    assert(kh)
                    new_v = frozenset(v.__dict__.items())
                    hashable[k] = new_v
            return hashable
        except Exception as e:
            raise e

    def serialize(self):
        try:
            p = pickle.dumps(self.__dict__)
            return p.encode(encoding='UTF-8')
        except RecursionError as e:
            p = pickle.dumps({'serialize_error': e})
            return p.encode(encoding='UTF-8')
        except TypeError as e:
            p = pickle.dumps({'serialize_error': e})
            return p.encode(encoding='UTF-8')
        except Exception as e:
            p = pickle.dumps({'serialize_error': e})
            return p.encode(encoding='UTF-8')

    def marshall(self):
        try:
            j = jsonpickle.dumps(self.__dict__)
            return j.encode(encoding='UTF-8')
        except RecursionError as e:
            j =  jsonpickle.dumps({'marshall_error': e})
            return j.encode(encoding='UTF-8')
        except TypeError as e:
            j =  jsonpickle.dumps({'marshall_error': e})
            return j.encode(encoding='UTF-8')
        except Exception as e:
            j =  jsonpickle.dumps({'marshall_error': e})
            return j.encode(encoding='UTF-8')

    def dump(self):
        try:
            j = self.marshall()
            jd = hashlib.sha1(j).hexdigest()
            p = self.serialize()
            pd = hashlib.sha1(p).hexdigest()
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
