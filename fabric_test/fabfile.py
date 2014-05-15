#coding=utf8
#!/usr/bin/python
from fabric.api import env, run, cd, open_shell, execute, roles
from fabric.context_managers import *	#上下文环境管理，主要使用with语句
import sys

env.roledefs = {'web1':['yy@211.155.86.145:22'],'web2':['yanfa@192.168.16.66:22'],'web3':['yy@10.1.6.159:22']}
# env.hosts=['211.155.86.145','192.168.16.66']
env.passwords = {'yy@211.155.86.145:22':"yy123",'yanfa@192.168.16.66:22':"123456",'yy@10.1.6.159:22':"yy123"}
env.exclude_hosts = ['yy@10.1.6.159:22']

@roles('web1')
def task1():
    with cd('/home/yy'):
        text1 = run('pwd')
        print '*****************************************'
        text2 = run('ls')
        print '*****************************************'
        with cd('Python-2.7.6'):
	        text3 = run('pwd')
	        print '*****************************************'
	        text4 = run('ls -l')
	        print '*****************************************'
	# print text1,text2,text3,text4

@roles('web2')
def task2():
    with cd('/home/yanfa'):
        text1 = run('pwd')
        print '*****************************************'
        text2 = run('ls')
        print '*****************************************'
        
@roles('web3')
def task3():
    open_shell("ifconfig eth0|grep '10.1.6.159'")

def deploy():
    execute(task1)
    execute(task2)

# from fabric.colors import *
# print(green("This text is green!"))


# fabric.decorators.serial(func) （串行执行，不允许并行）强制func串行执行
# fabric.decorators.parallel(pool_size=None) （并行执行，而不是串行）
# fabric.utils.warn(msg)打印警告信息，但是不放弃执行
# confirm(询问用户问题，返回 Y/N，比如“是否继续”这样的问题)
# fabric.network.disconnect_all()

# fabric.operations.get(remote_path, local_path=None)	#Download one or more files from a remote host.remote
# fabric.operations.prompt(text, key=None, default='', validate=None)	#Prompt user with text and return the input (like raw_input)
# fabric.operations.put(local_path=None, remote_path=None, use_sudo=False,mirror_local_mode=False, mode=None)	#Upload one or more files to a remote host
# fabric.operations.reboot(wait=120)
# fabric.operations.sudo(command, shell=True, pty=True, combine_stderr=None, user=None, quiet=False, warn_only=False, stdout=None, stderr=None, group=None)	#Run a shell command on a remote host, with superuser privileges.
# fabric.context_managers.path(path, behavior='append')	#Append the given path to the PATH
# fabric.context_managers.prefix(command)	#Prefix all wrapped run/sudo commands with given command plus &&.
# fabric.context_managers.settings(*args, **kwargs)	#Nest context managers and/or override env variables
# fabric.contrib.project.rsync_project(*args, **kwargs)	#Synchronize a remote directory with the current project directory via rsync
# fabric.contrib.project.upload_project(local_dir=None, remote_dir='')	#Upload the current project to a remote system via tar/gzip
#














