# lldb_python


https://lldb.llvm.org/python-reference.html

1、lldb调试器导入python脚本，可以直接在调试器中执行，立马能用
command script import python-script路径

2、对于经常使用的脚本，可以在lldb的初始化文件里添加命令加载脚本，启动自定义的命令，修改~/.lldbinit文件，在文件里加入一行

3、添加命令sbr

command script add sbr -f lldb_about.sbr
