#!/usr/bin/env python3
# Errors:
# 1: Required argument not specified
# 2: Camouflage path not found
# 3: Invalid arguement
# 4: Invalid server string
# 5: No connection info saved in ~/.gekko
import os, re, sys, getopt

def showhelp():
    strHelp = """
Gekko - Makes SFTP upload "easy-peasy lizard squeezy".

Usage: gekko <command> [<args>]

Commands listed below:
   camo     Define a file or a directory which will be ignored
            when uploading. This will generate '.gekkoign' file
   grip     Define a host which files will be uploaded to. You
            can also save the host or remove it
   sense    Show the changes which will be taken
   run      Start the upload sequence
"""
    print(strHelp)

def bootstrapper():
    if len(sys.argv) < 2:
        showhelp()
    else:
        if sys.argv[1] == "camo":
            if len(sys.argv) == 2:
                print("Specify path of a file or directory to ignore.")
                exit(1)
            else:
                camouflage(sys.argv[2])
        elif sys.argv[1] == "grip":
            if len(sys.argv) == 2:
                print("Specify SFTP connection info.")
                exit(1)
            else:
                if len(sys.argv) == 3:
                    print("No arguement found.")
                    exit(1)
                else:
                    try:
                        opts, args = getopt.getopt(sys.argv[3:], "s:rl")
                        opt = opts[0][0]
                        val = opts[0][1]
                        if opt == '-s':
                            grip(sys.argv[2], val)
                        elif opt == '-l':
                            listconn(sys.argv[2])
                        elif opt == '-r':
                            removeconn(sys.argv[2])
                    except getopt.GetoptError:
                        print("Invalid arguement.")
                        exit(3)

        elif sys.argv[1] == "sense":
            if len(sys.argv) == 2:
                print("Specify connection remark.")
                exit(1)
            else:
                sense(sys.argv[2])

        elif sys.argv[1] == "run":
            if len(sys.argv) == 2:
                print("Specify connection remark.")
                exit(1)
            else:
                run(sys.argv[2])
        else:
            showhelp()

def camouflage(path):
    print("Checking for %s..." % path, end='')
    if os.path.exists(path):
        print(" Exist.")
        root = os.path.dirname(os.path.abspath(path))
        ignfile = os.path.join(root, ".gekkoign")
        with open(ignfile, 'a', encoding='UTF-8') as f:
            f.write(path + '\n')
        print("%s saved." % ignfile)
    else:
        print(" Not exist.")
        print("The path you specified does not exist.")
        exit(2)

def grip(server_string, remark):
    if re.match("[a-z]*@.*:[0-9]+#.*", server_string) == None:
        print("Invalid server string.")
    else:
        user = server_string.split('@')[0]
        host = server_string.split('@')[1].split(':')[0]
        port = server_string.split('@')[1].split(':')[1].split('#')[0]
        path = server_string.split('@')[1].split(':')[1].split('#')[1]
        print("Host:             %s" % host)
        print("SSH Port:         %s" % port)
        print("User:             %s" % user)
        print("Upload Directory: %s" % path)
        print("Remark:           %s" % remark)
        svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
        with open(svrfile, 'r', encoding='UTF-8') as fr:
            lines = fr.readlines()
        with open(svrfile, 'w', encoding='UTF-8') as f:
            for line in lines:
                if remark in line:
                    continue
                else:
                    f.write(line)
            f.write(remark + '=' + server_string + '\n')
        print("\nConnection Saved.")

def listconn(remark):
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("No connection info was saved.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as fr:
        lines = fr.readlines()
    if lines == None:
        print("No connection info was saved.")
        exit(5)
    for line in lines:
        if line.startswith(remark):
            user = line.split('=')[1].split('@')[0]
            host = line.split('@')[1].split(':')[0]
            port = line.split('@')[1].split(':')[1].split('#')[0]
            path = line.split('@')[1].split(':')[1].split('#')[1]
            print("Host:             %s" % host)
            print("SSH Port:         %s" % port)
            print("User:             %s" % user)
            print("Upload Directory: %s" % path.strip('\n'))
            print("Remark:           %s" % remark)
            exit(0)
    print("Cannot for connection info with remark '%s'." % remark)

def removeconn(remark):
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("No connection info was saved.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as fr:
        lines = fr.readlines()
    if lines == None:
        print("No connection info was saved.")
        exit(5)
    with open(svrfile, 'w', encoding='UTF-8') as f:
        for line in lines:
            if remark in line:
                continue
            else:
                f.write(line)
    print("Done.")

def sense(remark):
    print("Sense %s" % remark)

def run(remark):
    print("Run %s" % remark)

if __name__ == "__main__":
    bootstrapper()
