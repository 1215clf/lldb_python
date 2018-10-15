#!/usr/bin/python

import commands
import optparse
import lldb
import shlex
import re
import os


def iobjc_msgSend(debugger, command, result, internal_dict):
    interpreter = lldb.debugger.GetCommandInterpreter()
    returnObject = lldb.SBCommandReturnObject()
    thread = debugger.GetSelectedTarget().GetProcess().GetSelectedThread()
    thread.StepOver()
    while True:
        interpreter.HandleCommand('dis -p -c 10', returnObject)
        disassemble = returnObject.GetOutput();
        p = re.compile(r'->.*')
        m = p.search(disassemble)
        c = m.group(0)
        if 'objc_msgSend' in c:
            print('objc_msgSend Hited!')
            print(disassemble)
            break
        else:
            thread.StepOver()


def iobjc_msgSended(debugger, command, result, internal_dict):
    iobjc_msgSend(debugger, command, result, internal_dict)
    interpreter = lldb.debugger.GetCommandInterpreter()
    returnObject = lldb.SBCommandReturnObject()
    thread = debugger.GetSelectedTarget().GetProcess().GetSelectedThread()
    thread.StepOver()
    print('objc_msgSend Evaluated!')

    interpreter.HandleCommand('dis -s `$pc-0x8` -c 5', returnObject)
    disassemble = returnObject.GetOutput()
    print(disassemble)

    iprint_args(debugger, command, result, internal_dict)

    interpreter.HandleCommand('po $x0', returnObject)
    ret = returnObject.GetOutput().strip()
    print('Return Value: %s' % ret)


def iprint_args(debugger, command, result, internal_dict):
    interpreter = lldb.debugger.GetCommandInterpreter()
    returnObject = lldb.SBCommandReturnObject()
    interpreter.HandleCommand('po $x0', returnObject)
    arg1 = returnObject.GetOutput().strip()
    interpreter.HandleCommand('p (char *)$x1', returnObject)
    arg2 = returnObject.GetOutput().strip()

    print('-[%s %s]' % (arg1, arg2))

    functionName = '['
    functionName += '%s ' % arg1
    p = re.compile('"(.*)"')
    m = p.search(arg2)
    if m is not None:
        s = m.group(1)
        names = s.split(':')
        print(names)
        for i in range(len(names) - 1):
            interpreter.HandleCommand('po $x%d' % (i + 2), returnObject)
            value = returnObject.GetOutput().strip()
            name = names[i]
            functionName += ' %s:%s ' % (name, value)

    functionName += ']'
    print('functionName',functionName)


def __lldb_init_module(debugger, dict):
    names = ['iobjc_msgSend', 'iobjc_msgSended', 'iprint_args']
    helpTexts = ["Break at next objc_msgSend.", "Evaluate next objc_msgSend.", "Print current objc_msgSend arguments."]
    for i in range(len(names)):
        name = names[i]
        helpText = helpTexts[i]
        debugger.HandleCommand('command script add %s -f %s.%s' % (name, __name__, name))
        print('The "%s" python command has been installed and is ready for use.' % name)
        debugger.HandleCommand(
            'command script add --help "{help}" --function {function} {name}'.format(help=helpText, function=name,
                                                                                     name=name))