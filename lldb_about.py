#!/usr/bin/python
#coding:utf-8


'''
https://lldb.llvm.org/python-reference.html
    
1、lldb调试器导入python脚本，可以直接在调试器中执行，立马能用
command script import python-script路径

2、对于经常使用的脚本，可以在lldb的初始化文件里添加命令加载脚本，启动自定义的命令，修改~/.lldbinit文件，在文件里加入一行

3、添加命令sbr

command script add sbr -f lldb_about.sbr

'''

import lldb
import commands
import optparse
import shlex
import re


# 获取ASLR偏移地址
def get_ASLR():
    # 获取'image list -o'命令的返回结果
    interpreter = lldb.debugger.GetCommandInterpreter()
    returnObject = lldb.SBCommandReturnObject()
    interpreter.HandleCommand('image list -o', returnObject)
    output = returnObject.GetOutput()
    # 正则匹配出第一个0x开头的16进制地址
    match = re.match(r'.+(0x[0-9a-fA-F]+)', output)
    if match:
        print('ALSR',match.group(1))
        # return match.group(2)
        return match.group(1)
    else:
        # print('ALSR None')
        return None

# Super breakpoint
def sbr(debugger, command, result, internal_dict):

    #用户是否输入了地址参数
    if not command:
        print(result, 'Please input the address!')
        return

    ASLR = get_ASLR()
    if ASLR:
        #如果找到了ASLR偏移，就设置断点
        debugger.HandleCommand('br set -a "%s+%s"' % (ASLR, command))
    else:
        print(result, 'ASLR not found!')


# memory read --size 8 --format x address命令
def mrd(debugger, command, result, internal_dict):
    debugger.HandleCommand('memory read --size 8 --format x %s'% command)
    # print('result',result)

    # interpreter = lldb.debugger.GetCommandInterpreter()
    # returnObject = lldb.SBCommandReturnObject()
    # interpreter.HandleCommand('memory read --size 8 --format x %s'% command, returnObject)
    # output = returnObject.GetOutput()
    # print(output)



# And the initialization code to add your commands
#一旦Python模块被加载到LLDB中时它就会被调用
def __lldb_init_module(debugger, internal_dict):
    # 'command script add sbr' : 给lldb增加一个'sbr'命令
    # '-f lldb_about.sbr' : 该命令调用了lldb_about文件的sbr函数
    # -f参数表明你想要绑定一个Python函数命令.
    # 也可以写成 command script add -f lldb_about.sbr sbr
    debugger.HandleCommand('command script add sbr -f lldb_about.sbr')
    print('The "sbr" python command has been installed and is ready for use.')
    debugger.HandleCommand('command script add mrd -f lldb_about.mrd')
    print('The "mrd" python command has been installed and is ready for use.')
