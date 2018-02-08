#!/usr/bin/env python3
# Errors:
# 1: Required argument not specified
# 2: Camouflage path not found
import os, sys, getopt

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
            print('grip')
        elif sys.argv[1] == "sense":
            print('sense')
        elif sys.argv[1] == "run":
            print('run')
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
        print("Error: the path you specified does not exist.")
        exit(2)

def grip(**kwargs):
    pass

def sense():
    pass

def run():
    pass

if __name__ == "__main__":
    bootstrapper()
