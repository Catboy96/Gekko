#!/usr/bin/env python3
# Errors:
# 1: Required argument not specified
# 2: Camouflage path not found
# 3: Invalid arguement
# 4: Invalid server string
# 5: No connection info saved in ~/.gekko
# 6: Cannot find connection info with specified remark
import os, re, sys, getopt, pysftp, paramiko

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
        elif sys.argv[1] == "camouflage":
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
                try:
                    opts, args = getopt.getopt(sys.argv[3:], "p:")
                    if not len(opts) == 0:
                        run(sys.argv[2], opts[0][1])
                    else:
                        run(sys.argv[2], "")
                except getopt.GetoptError:
                    print("Specify password for '-p' option.")
                    exit(3)
        else:
            showhelp()

def camouflage(path):
    print("Checking for %s..." % path, end='')
    if os.path.exists(path):
        print(" Exist.")
        root = os.path.abspath(os.curdir)
        ignfile = os.path.join(root, ".gekkoign")
        print(ignfile)
        if os.path.exists(ignfile):
            with open(ignfile, 'r', encoding='UTF-8') as fr:
                lines = fr.readlines()
            with open(ignfile, 'w', encoding='UTF-8') as f:
                for line in lines:
                    if path in line:
                        continue
                    else:
                        f.write(line)
                f.write(path + '\n')
        else:
            with open(ignfile, 'w', encoding='UTF-8') as f:
                f.write(path + '\n')
        print("%s saved." % ignfile)
    else:
        print(" Not exist.")
        print("The path you specified does not exist.")
        exit(2)

def grip(server_string, remark):
    matchobj = re.match(r'^([a-z0-9_]{1,32})@(\S+):(\d{1,5})#(\S+)$', server_string)
    if not matchobj:
        print("Invalid server string.")
    else:
        user = matchobj.group(1)
        host = matchobj.group(2)
        port = matchobj.group(3)
        path = matchobj.group(4)
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
    print("Cannot find connection info with remark '%s'." % remark)
    exit(6)

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

def run(remark, password):

    # Get connection info
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("No connection info was saved.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as fr:
        lines = fr.readlines()
    if lines == None:
        print("No connection info was saved.")
        exit(5)
    user, host, port, path = '', '', '', ''
    for line in lines:
        if line.startswith(remark):
            user = line.split('=')[1].split('@')[0]
            host = line.split('@')[1].split(':')[0]
            port = line.split('@')[1].split(':')[1].split('#')[0]
            path = line.split('@')[1].split(':')[1].split('#')[1].strip('\n')
    if user == '' or host == '' or port == '' or path == '':
        print("Cannot find connection info with remark '%s'." % remark)
        exit(6)
    if password == '':
        password = input("SSH Password of %s: " % host)

    # Get Ignored files
    root = os.path.abspath(os.curdir)
    ignfile = os.path.join(root, ".gekkoign")
    with open(ignfile, 'r', encoding='UTF-8') as fr:
        lines = fr.read().split('\n')
        while '' in lines:
            lines.remove('')

    # Establish connection
    try:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        print("Connecting to %s:%s... " % (host, port), end='')
        sftp = pysftp.Connection(host, username=user, port=int(port), password=password, cnopts=cnopts)
        print("Connected.")
    except pysftp.exceptions.ConnectionException:
        print("\n\nAn error occured when establishing connection.\nCheck for Internet connection.")
    except paramiko.ssh_exception.AuthenticationException:
        print("\n\nAuthentication failed.")

    # Make & change directory
    print("Make directory at %s... " % path, end='')
    try:
        sftp.mkdir(path)
        print("Done.")
    except OSError:
        print("Skipped.")
    print("Change directory to %s... Done." % path)
    sftp.cd(path)

    # Check & Upload
    ignored = 0
    for dirname, subdirs, filenames in os.walk(root):
        for filename in filenames:
            rel = os.path.relpath(os.path.join(dirname, filename))
            for line in lines:
                if rel.startswith(line):
                    print("Ignored:   %s" % rel)
                    ignored = 1
                    break
                elif rel == '.gekkoign':
                    print("Ignored:   .gekkoign")
                    ignored = 1
                    break
                else:
                    ignored = 0
            if not ignored == 1:
                print("Uploading: %s... " % rel, end='')
                rpath = os.path.join(path, rel)
                try:
                    sftp.put(rel, remotepath=rpath, preserve_mtime=True)
                    print("Done.")
                except FileNotFoundError:
                    sftp.makedirs(os.path.dirname(rpath))
                    sftp.put(rel, remotepath=rpath, preserve_mtime=True)
                    print("Done.")

    # Close connection
    print("Disconnecting... ", end='')
    sftp.close()
    print("Done.")
    print("\nOperation successfully completed.")

    


if __name__ == "__main__":
    bootstrapper()
