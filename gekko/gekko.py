#!/usr/bin/env python3
# Errors:
# 1: Required argument not specified
# 2: Camouflage path not found
# 3: Invalid arguement
# 4: Invalid server string
# 5: No connection info saved in ~/.gekko
# 6: Cannot find connection info with specified remark
import os, re, sys, pysftp, paramiko
import argparse
import yaml


def bootstrapper():
    # Create a parser
    parser = argparse.ArgumentParser(description='Gekko - Makes SFTP upload "easy-peasy lizard squeezy"')
    # Create sub-command parsers
    subparsers = parser.add_subparsers()

    # GEKKO CAMOUFLAGE ---
    parser_camo = subparsers.add_parser(
        'camouflage', aliases=['camo'], help='Define a file or a directory which will be ignored'
                     ' when uploading. This will generate \'.gekkoign\' file.')
    # Accept path param
    parser_camo.add_argument('path', help = 'the path of a file or directory to ignore')
    #once camouflage command matched, goto camouflage routine
    parser_camo.set_defaults(func=camouflage)

    # Make sub-commands
    # GEKKO GRIP ---
    parser_make = subparsers.add_parser(
        'grip', aliases=['gp'], help='Create a host which files will be uploaded to. You can also save the host or remove it')
    # Accept connection param
    parser_make.add_argument('connection', help='Specify the connection using user@hostname:path')
    # Accept remark param
    parser_make.add_argument('-s', dest='REMARK', help='The remark of connection to be created.')
    # Accept port param by the default value of 22, since default value of ssh port is 22
    parser_make.add_argument('-p', dest='PORT', type=int, default=22, help='ssh port')
    parser_make.add_argument('-k', dest='KEY', type=str, default='', help='Use a private key instead of a password.')
    parser_make.set_defaults(func=make)

    # GEKKO LIST
    parser_list = subparsers.add_parser(
        'list', aliases=['ls'], help='Show all the connections.')
    parser_list.set_defaults(func=list)

    # GEKKO REMOVE
    parser_remove = subparsers.add_parser(
        'remove', aliases=['rm'], help='Remove a connecion.')
    parser_remove.add_argument('REMARK', help='Specify the connection using remark')
    parser_remove.set_defaults(func=removeconn)

    # GEKKO RUN
    parser_run = subparsers.add_parser(
        'run', aliases=['rn'], help='Start the upload sequence.')
    parser_run.add_argument('REMARK', help='Specify the connection using remark')
    parser_run.add_argument('-p', dest='PASSWORD', default='', type=str, help='password')
    parser_run.set_defaults(func=upload)

    # GEKKO SENSE
    parser_run = subparsers.add_parser(
        'sense', aliases=['ss'], help='Check for the changes which will taken in uploading.')
    parser_run.add_argument('REMARK', help='Specify the connection using remark')
    parser_run.add_argument('-p', dest='PASSWORD', default='', type=str, help='password')
    parser_run.set_defaults(func=sense)

    # Parse
    args = parser.parse_args()
    try:
        # Call sub-command routine
        args.func(args)
    except AttributeError:
        # No arguements specified, show help.
        parser.print_help()
        exit(0)

def camouflage(args):
    print("Checking for %s..." % args.path, end='')
    if os.path.exists(args.path):
        print(" Exist.")
        root = os.path.abspath(os.curdir)
        ignfile = os.path.join(root, ".gekkoign")
        print(ignfile)
        if os.path.exists(ignfile):
            with open(ignfile, 'r', encoding='UTF-8') as fr:
                lines = fr.readlines()
            with open(ignfile, 'w', encoding='UTF-8') as f:
                for line in lines:
                    if args.path in line:
                        continue
                    else:
                        f.write(line)
                f.write(args.path + '\n')
        else:
            with open(ignfile, 'w', encoding='UTF-8') as f:
                f.write(args.path + '\n')
        print("%s saved." % ignfile)
    else:
        print(" Not exist.")
        print("The path you specified does not exist.")
        exit(2)

def make(args):
    matchobj = re.match(r'^([a-z0-9_]{1,32})@(\S+):(\S+)$', args.connection)
    if not matchobj:
        print("Invalid server string.")
    else:
        user = matchobj.group(1)
        host = matchobj.group(2)
        path = matchobj.group(3)
        print("Host:             %s" % host)
        print("SSH Port:         %s" % args.PORT)
        print("User:             %s" % user)
        print("Upload Directory: %s" % path)
        print("Remark:           %s" % args.REMARK)
        if args.KEY != '':
            print("Private key:      %s" % args.KEY)
        svrfile = os.path.join(os.path.expanduser('~'), ".gekko")

        #load connections
        data = []
        if os.path.exists(svrfile):
            with open(svrfile, 'r', encoding='UTF-8') as f:
                data = yaml.load(f)
        if not data:
            data = []
        item = [i for i in data if i['remark'] == args.REMARK]
        if not item:
            data.append({'remark': args.REMARK,
                         'host': host,
                         'user': user,
                         'path': path,
                         'port': args.PORT,
                         'key': args.KEY,
                         })
        else:
            item[0]['host'] = host
            item[0]['user'] = user
            item[0]['path'] = path
            item[0]['port'] = args.PORT
            item[0]['key'] = args.KEY
        with open(svrfile, 'w', encoding='UTF-8') as f:
            f.write(yaml.dump(data))
        print("\nConnection Saved.")

def list(args):
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("Gasping Gekkos! No connection saved yet.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as f:
        datas = yaml.load(f)
    if not datas:
        print('Gasping Gekkos! No connection saved yet.')
        exit(5)
    for data in datas:
        print('Remark:%s; connection:%s@%s:%s; ' % (data['remark'], data['user'], data['host'], data['path']), end='')
        if data['port'] != 22:
            print('port:%d; ' % data['port'], end='')
        if data['key'] != '':
            print('private_key:%s;' % data['key'], end='')
        print('')  #newline
    exit(0)

def removeconn(args):
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("No connection has saved.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as f:
        datas = yaml.load(f)
    if not datas:
        print('No connection has saved.')
        exit(5)
    for i in datas:
        if i['remark'] == args.REMARK:
            datas.remove(i)
    with open(svrfile, 'w', encoding='UTF-8') as f:
        f.write(yaml.dump(datas))
    print("Done.")

def sense(args):
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("No connection has saved.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as f:
        datas = yaml.load(f)
    if not datas:
        print('No connection has saved.')
        exit(5)
    password = args.PASSWORD
    for i in datas:
        if i['remark'] == args.REMARK:
            if i['key'] == '' and password == '':
                password = input("SSH Password of %s: " % i['host'])
            do_sense(i['user'], i['host'], i['port'], password, i['path'], i['key'])
            break

def do_sense(user, host, port, password, path, key):

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
        if key != '':
            sftp = pysftp.Connection(host, username=user, port=int(port), private_key=key, cnopts=cnopts)
        else:
            sftp = pysftp.Connection(host, username=user, port=int(port), password=password, cnopts=cnopts)
        print("Connected.")
    except pysftp.exceptions.ConnectionException:
        print("\n\nAn error occured when establishing connection.\nCheck for Internet connection.")
    except paramiko.ssh_exception.AuthenticationException:
        print("\n\nAuthentication failed.")

    # Check for uploading directory
    print("Checking for %s... " % path, end='')
    if sftp.exists(path):
        print("Exist.")
        print("Change directory to %s... Done." % path)
        sftp.cd(path)
    else:
        # Well, just print every file not ignored.
        print("Not exist.")
        print("Changes will be taken:\n")
        ignored = 0
        for dirname, subdirs, filenames in os.walk(root):
            for filename in filenames:
                rel = os.path.relpath(os.path.join(dirname, filename))
                for line in lines:
                    if rel.startswith(line):
                        ignored = 1
                        break
                    elif rel == '.gekkoign':
                        ignored = 1
                        break
                    else:
                        ignored = 0
                if not ignored == 1:
                    # 'rel'   will be local file relative path.
                    # 'rpath' will be remote file absolute path.
                    rpath = os.path.join(path, rel)
                    print("+ %s" % rpath)

        # Close connection
        print("\nDisconnecting... ", end='')
        sftp.close()
        print("Done.")
        exit(0)

    # Check which files are changed.
    print("Changes will be taken:\n")
    ignored = 0
    for dirname, subdirs, filenames in os.walk(root):
        for filename in filenames:
            rel = os.path.relpath(os.path.join(dirname, filename))
            for line in lines:
                if rel.startswith(line):
                    ignored = 1
                    break
                elif rel == '.gekkoign':
                    ignored = 1
                    break
                else:
                    ignored = 0
            if not ignored == 1:
                # 'rel'   will be local file relative path.
                # 'rpath' will be remote file absolute path.
                rpath = os.path.join(path, rel)
                # Try getting remote file info.
                try:
                    fr = sftp.lstat(rpath)
                    fl = os.stat(rel)
                    # If remote file's modification time & size equals to the
                    # local file, means the file is not changed.
                    if fr.st_size == fl.st_size and int(fr.st_mtime) == int(fl.st_mtime):
                        pass
                    else:
                        # The file is changed.
                        print("* %s" % rpath)
                except:
                    # Remote file doesn't exist. Needs to upload.
                    print("+ %s" % rpath)

    # Close connection
    print("\nDisconnecting... ", end='')
    sftp.close()
    print("Done.")

def upload(args):
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("No connection has saved.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as f:
        datas = yaml.load(f)
    if not datas:
        print('No connection has saved.')
        exit(5)
    password = args.PASSWORD
    for i in datas:
        if i['remark'] == args.REMARK:
            if i['key'] == '' and password == '':
                password = input("SSH Password of %s: " % i['host'])
            upload_files(i['user'], i['host'], i['port'], password, i['path'], i['key'])
            break

def upload_files(user, host, port, password, path, key):

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
        if key != '':
            sftp = pysftp.Connection(host, username=user, port=int(port), private_key=key, cnopts=cnopts)
        else:
            sftp = pysftp.Connection(host, username=user, port=int(port), password=password, cnopts=cnopts)
        print("Connected.")
    except pysftp.exceptions.ConnectionException:
        print("\n\nAn error occured when establishing connection.\nCheck for Internet connection.")
    except paramiko.ssh_exception.AuthenticationException:
        print("\n\nAuthentication failed.")

    # Check for uploading directory
    print("Checking for %s... " % path, end='')
    if sftp.exists(path):
        print("Exist.")
        print("Change directory to %s... Done." % path)
        sftp.cd(path)
    else:
        print("Not exist.")
        print("Make directory at %s... " % path, end='')
        sftp.makedirs(path)
        print("Done.")

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

                # 'rel'   will be local file relative path.
                # 'rpath' will be remote file absolute path.
                rpath = os.path.join(path, rel)
                # Try getting remote file info.
                try:
                    fr = sftp.lstat(rpath)
                    fl = os.stat(rel)
                    # If remote file's modification time & size equals to the
                    # local file, then skip it.
                    if fr.st_size == fl.st_size and int(fr.st_mtime) == int(fl.st_mtime):
                        print("Skipped:   %s" % rel)
                    else:
                        # Upload it, cause it changed!
                        print("Uploading: %s... " % rel, end='')
                        try:
                            sftp.put(rel, remotepath=rpath, preserve_mtime=True)
                            print("Done.")
                        except:
                            print("FAILED.")
                except:
                    # Remote file doesn't exist. Upload directly.
                    print("Uploading: %s... " % rel, end='')
                    try:
                        sftp.put(rel, remotepath=rpath, preserve_mtime=True)
                        print("Done.")
                    except FileNotFoundError:
                        # Build remote file's path if nessesary.
                        sftp.makedirs(os.path.dirname(rpath))
                        sftp.put(rel, remotepath=rpath, preserve_mtime=True)
                        print("Done.")

    # Close connection
    print("Disconnecting... ", end='')
    sftp.close()
    print("Done.")
