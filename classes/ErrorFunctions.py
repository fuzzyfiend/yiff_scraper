#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

def debugOutput(k, v, t, prompt="[<>]", header="stack variable"):
    print("%s %s: (%s) is of type (%s) and is (%s)" % (prompt, header, str(k), str(t), str(v)))

# Given name => dict, print details about name, and each row of dict
def debugDict(dic_name, dic_dict, prompt="[<>]", header="stack variable"):
    print( "%s %s: (%s) is of len (%d)" % (prompt, header, dic_name, len(dic_dict)) )
    for k,v in dic_dict.items():
        print("%s %s: (%s) is of type (%s) and is (%s)" % (prompt, 'dict contents', str(k), str(type(v)), str(v)))

def debugList(lst_name, lst_list, prompt="[<>]", header="stack variable"):
    print( "%s %s: (%s) is of len (%d)" % (prompt, header, lst_name, len(lst_list)) )
    k = 0
    for v in lst_list:
        print("%s %s: index[%d] is of type (%s) and is (%s)" % (prompt, 'list contents', k, type(v), str(v)))
        k = k + 1

def handleBacktrace(stack):
    for k,v in stack.items():
        print("[<>] Handling variable [%s]" % k)

        if type(v) is dict:
            debugDict(k, v)
        elif type(v) is list:
            debugList(k, v)
        elif isinstance(v, Exception):
            debugOutput(k, v, type(v), "[<>]")
        else:

            try:
                ## Try to call dump
                d  = v.dump()
                print("[<>] --> calling member.dump(), trace to follow")
                debugDict(v.__class__, d, "[<!>]", ">> member variable")
            except AttributeError:
                ## try to call __dict__
                d = v.__dict__
                print("[<>] --> iterating over member.__dict__, trace to follow")
                debugDict(v.__class__, d, "[<!>]", ">> member variable")
            finally:
                ## regardless, dump the variable out if primitive
                debugOutput(k, v, type(v), "[<>]")
                print()
