#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from commandr import command, Run


servers = {}


def load_server():
    global servers, servers_file, command_path

    command_path = os.path.dirname(os.path.realpath(__file__))
    servers_file = "%s/conf/server" % command_path

    try:
        if not os.path.exists(servers_file):
            fo = file(servers_file, 'w')
            fo.close()
        else:
            fi = file(servers_file, 'r')
            content = fi.read()
            fi.close()

            lines = content.strip().split('\n')
            for line in lines:
                (server_name, server, port, user, password, note) = line.split(',')
                servers[server_name] = {"server": server, "port": port, "user": user, "password": password,
                                        "note": note}
    except IOError, e:
        print "Error in reading %s with error code %d: %s" %(servers_file, e.args[0],e.args[1])
        exit(1)


def check_server_name(server_name):
    if server_name not in servers:
        print "server name is not exist"
        exit()

@command('ssh')
def ssh(server_name):
    check_server_name(server_name)
    server = servers[server_name]
    command = "sshpass -p %s ssh -p %s %s@%s" % (server["password"], server["port"], server["user"], server["server"])
    os.system(command)


@command('push')
def scp(server_name, local_file, remote_path = "~/"):
    check_server_name(server_name)
    server = servers[server_name]
    command = "sshpass -p %s scp -C -P %s %s %s@%s:%s" % (server["password"], server["port"], local_file,
                                                          server["user"], server["server"], remote_path)
    os.system(command)


@command('pull')
def scp(server_name, remote_file, local_path = "~/"):
    check_server_name(server_name)
    server = servers[server_name]
    command = "sshpass -p %s scp -C -P %s %s@%s:%s %s" % (server["password"], server["port"], server["user"],
                                                       server["server"], remote_file, local_path)
    os.system(command)


@command('list')
def scp():
    for server in servers:
        print("%s:%s" % (server, str(servers[server]).replace("'", "")))


@command('add')
def add():
    print("wait...")


@command('remove')
def remove(server_name):
    print("wait...")


if __name__ == "__main__":
    load_server()
    Run()



