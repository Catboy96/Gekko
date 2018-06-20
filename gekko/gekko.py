#!/usr/bin/env python3

import os
import re
import pysftp
import paramiko
import argparse
import getpass
import yaml
import warnings
import random
import configparser

__VERSION__ = "1.0.0"

warnings.filterwarnings("ignore")


def bootstrapper():
    parser = argparse.ArgumentParser(description='Gekko - Makes SFTP synchronization "easy-peasy lizard squeezy"')
    subparsers = parser.add_subparsers()

    # GEKKO CAMOUFLAGE
    parser_camo = subparsers.add_parser('camouflage', aliases=['camo'],
                                        help='Define a file or a directory which will be ignored'
                                             ' when syncing. This will generate \'.gekkoign\' file.')
    parser_camo.add_argument('path', help='the path of a file or directory to ignore')
    parser_camo.set_defaults(func=do_camouflage)

    # GEKKO GRIP
    parser_grip = subparsers.add_parser('grip', aliases=['gp'],
                                        help='Create a host which files will be uploaded to. You can also save the '
                                             'host or remove it')
    parser_grip.add_argument('connection', help='Specify the connection using user@hostname:path')
    parser_grip.add_argument('-s', dest='REMARK', help='The remark of connection to be created.')
    parser_grip.add_argument('-p', dest='PORT', type=int, default=22, help='ssh port')
    parser_grip.add_argument('-k', dest='KEY', type=str, default='', help='Use a private key instead of a password.')
    parser_grip.add_argument('-l', dest='LOCAL', type=str, default='', help='Specify a local path.')
    parser_grip.set_defaults(func=do_grip)

    # GEKKO LIST
    parser_list = subparsers.add_parser('list', aliases=['ls'], help='Show all the connections.')
    parser_list.set_defaults(func=do_list)

    # GEKKO REMOVE
    parser_remove = subparsers.add_parser('remove', aliases=['rm'], help='Remove a connection.')
    parser_remove.add_argument('REMARK', help='Specify the connection using remark')
    parser_remove.set_defaults(func=do_remove)

    # GEKKO RUN
    parser_run = subparsers.add_parser('run', aliases=['rn'], help='Start the synchronization sequence.')
    parser_run.add_argument('REMARK', help='Specify the connection using remark')
    parser_run.add_argument('-p', dest='PASSWORD', default='', type=str, help='Password')
    parser_run.add_argument('-f', action='store_true', dest='FULLSYNC', default=False,
                            help='Remove all remote files and sync with local.')
    parser_run.set_defaults(func=run)

    # GEKKO SENSE
    parser_sense = subparsers.add_parser('sense', aliases=['ss'],
                                         help='Check for the changes which will taken in syncing.')
    parser_sense.add_argument('REMARK', help='Specify the connection using remark')
    parser_sense.add_argument('-p', dest='PASSWORD', default='', type=str, help='Password')
    parser_sense.set_defaults(func=sense)

    # GEKKO VERSION
    parser_ver = subparsers.add_parser('version', aliases=['ver'], help='Show the version of Gekko.')
    parser_ver.set_defaults(func=do_version)

    # GEKKO MUSCLE
    parser_muscles = subparsers.add_parser('muscles', help='???')
    parser_muscles.set_defaults(func=do_muscles)

    # Parse
    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
        exit(0)


def sense(args):
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("Gasping Geckos! No connection saved yet.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as f:
        data_collection = yaml.load(f)
    if not data_collection:
        print('Gasping Geckos! No connection saved yet.')
        exit(5)
    password = args.PASSWORD
    for i in data_collection:
        if i['remark'] == args.REMARK:
            if i['key'] == '' and password == '':
                password = getpass.getpass("SSH Password of %s: " % i['host'])
            do_sense(i['user'], i['host'], i['port'], password, i['path'], i['key'], i['local'])
            exit(0)
    print('Wriggling reptiles! "%s" seems not exist.' % args.REMARK)
    exit(6)


def run(args):
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("Gasping Geckos! No connection saved yet.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as f:
        data_collection = yaml.load(f)
    if not data_collection:
        print('Gasping Geckos! No connection saved yet.')
        exit(5)
    password = args.PASSWORD
    fullsync = args.FULLSYNC
    for i in data_collection:
        if i['remark'] == args.REMARK:
            if i['key'] == '' and password == '':
                password = getpass.getpass("SSH Password of %s: " % i['host'])
            do_run(i['user'], i['host'], i['port'], password, i['path'], i['key'], fullsync, i['local'])
            exit(0)
    print('Wriggling reptiles! "%s" seems not exist.' % args.REMARK)
    exit(6)


def gekko_feels(mood, exception):
    mood_file = os.path.join(os.path.expanduser('~'), ".gekko_mood")
    ini = configparser.ConfigParser()
    if not os.path.exists(mood_file):
        ini['mood'] = {'status': 'great'}
        ini['count'] = {'success': 0, 'failure': 0}
        ini['last'] = {'exception': 0}
    else:
        ini.read(mood_file)
    if mood == 'great':
        ini.set('mood', 'status', 'great')
        success_count = ini.get('count', 'success') + 1
        ini.set('count', 'success', success_count)
    elif mood == 'bad':
        ini.set('mood', 'status', 'bad')
        failure_count = ini.get('count', 'failure') + 1
        ini.set('count', 'failure', failure_count)
        ini.set('last', 'exception', exception)
    with open(mood_file, 'w') as f:
        ini.write(f)


def do_version():
    print("Gekko %s" % __VERSION__)


def do_muscles():
    voice_lines_negative = ('Gasping geckos! ', 'Wriggling reptiles! ', 'Slithering serpents! ')
    voice_lines_positive = ('Cool chameleons! ', 'Leaping lizards! ')
    mood_file = os.path.join(os.path.expanduser('~'), ".gekko_mood")
    if not os.path.exists(mood_file):
        print(random.choice(voice_lines_negative), end='')
        print("Haven't seen my Super Gekko Powers?")
        print('Then try me!')
        exit(0)
    ini = configparser.ConfigParser()
    ini.read(mood_file)
    mood = ini.get('mood', 'status')
    if mood == 'great':
        print(random.choice(voice_lines_positive), end='')
    elif mood == 'bad':
        print(random.choice(voice_lines_negative), end='')


def do_camouflage(args):
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


def do_grip(args):
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
        if args.LOCAL != '':
            print("Local path:       %s" % args.LOCAL)
        svrfile = os.path.join(os.path.expanduser('~'), ".gekko")

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
                         'local': args.LOCAL,
                         })
        else:
            item[0]['host'] = host
            item[0]['user'] = user
            item[0]['path'] = path
            item[0]['port'] = args.PORT
            item[0]['key'] = args.KEY
            item[0]['local'] = args.LOCAL
        with open(svrfile, 'w', encoding='UTF-8') as f:
            f.write(yaml.dump(data))
        print("\nConnection Saved.")


def do_list():
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("Gasping Geckos! No connection saved yet.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as f:
        data_collection = yaml.load(f)
    if not data_collection:
        print('Gasping Geckos! No connection saved yet.')
        exit(5)
    print('{:<20}'.format('Remarks'), end='')
    print('Connection')
    print('{:<20}'.format('-------'), end='')
    print('-------')
    for data in data_collection:
        print('{:<20}'.format(data['remark']), end='')
        print('%s@%s:%s ' % (data['user'], data['host'], data['path']), end='')
        if data['port'] != 22:
            print('-p %d ' % data['port'], end='')
        if data['key'] != '':
            print('-k %s' % data['key'], end='')
        if data['local'] != '':
            print('-l %s' % data['local'], end='')
        print('')
    exit(0)


def do_remove(args):
    svrfile = os.path.join(os.path.expanduser('~'), ".gekko")
    if not os.path.exists(svrfile):
        print("Gasping Geckos! No connection saved yet.")
        exit(5)
    with open(svrfile, 'r', encoding='UTF-8') as f:
        data_collection = yaml.load(f)
    if not data_collection:
        print('Gasping Geckos! No connection saved yet.')
        exit(5)
    for i in data_collection:
        if i['remark'] == args.REMARK:
            data_collection.remove(i)
    with open(svrfile, 'w', encoding='UTF-8') as f:
        f.write(yaml.dump(data_collection))
    print('"%s" removed.' % args.REMARK)


def do_sense(user, host, port, password, path, key, local):
    # Get Ignored files
    if local != '':
        os.chdir(local)
    root = os.path.abspath(os.curdir)
    ignfile = os.path.join(root, ".gekkoign")
    lines = []
    try:
        with open(ignfile, 'r', encoding='UTF-8') as fr:
            lines = fr.read().split('\n')
            while '' in lines:
                lines.remove('')
    except FileNotFoundError:
        lines = []

    # Establish SFTP connection
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
        print("\n\nAn error occurred when establishing connection.\nCheck for Internet connection.")
        exit(8)
    except paramiko.ssh_exception.AuthenticationException:
        print("\n\nAuthentication failed.")
        exit(7)

    # Check for uploading directory
    print("Checking for %s... " % path, end='')
    if sftp.exists(path):
        print("Exist.")
        print("Change directory to %s... Done." % path)
        sftp.cd(path)
    else:
        # Remote directory do not exist
        # Print every file not marked as 'ignored'
        total_size = 0
        print("Not exist.")
        print("Changes will be taken:")
        ignored = 0
        for dirname, subdirs, filenames in os.walk(root):
            for filename in filenames:
                rel = os.path.relpath(os.path.join(dirname, filename))
                if not lines:
                    ignored = 0
                else:
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
                    total_size += os.path.getsize(rel)
                    rpath = os.path.join(path, rel)
                    print("+ %s" % rpath)

        # Close connection
        print("Disconnecting... ", end='')
        sftp.close()
        print("Done.\n")
        print('%.3f MB need to upload.' % (total_size/1024/1024))
        exit(0)

    # Check which files are changed.
    print("Changes will be taken:")
    upload_size = 0
    ignored = 0
    for dirname, subdirs, filenames in os.walk(root):
        for filename in filenames:
            rel = os.path.relpath(os.path.join(dirname, filename))
            if not lines:
                ignored = 0
            else:
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

                # If remote file does not exists
                if not sftp.exists(rpath):
                    upload_size += os.path.getsize(rel)
                    print("+ %s" % rpath)
                    continue

                # Gather information of remote file
                fr = sftp.lstat(rpath)
                fl = os.stat(rel)

                # If remote file's modification time & size is the same as the
                # local one, stands the file is unchanged.
                if fr.st_size == fl.st_size and int(fr.st_mtime) == int(fl.st_mtime):
                    pass
                else:
                    # Upload.
                    upload_size += os.path.getsize(rel)

    # Close the connection
    print("Disconnecting... ", end='')
    sftp.close()
    print("Done.\n")
    print('%.3f MB need to upload.' % (upload_size/1024/1024))


def do_run(user, host, port, password, path, key, fullsync, local):
    # Get Ignored files
    if local != '':
        os.chdir(local)
    root = os.path.abspath(os.curdir)
    ignfile = os.path.join(root, ".gekkoign")
    lines = []
    try:
        with open(ignfile, 'r', encoding='UTF-8') as fr:
            lines = fr.read().split('\n')
            while '' in lines:
                lines.remove('')
    except FileNotFoundError:
        lines = []

    # Establish connection
    try:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        cnopts.compression = True
        print("Connecting to %s:%s... " % (host, port), end='')
        if key != '':
            sftp = pysftp.Connection(host, username=user, port=int(port), private_key=key, cnopts=cnopts)
        else:
            sftp = pysftp.Connection(host, username=user, port=int(port), password=password, cnopts=cnopts)
        print("Connected.")
    except pysftp.exceptions.ConnectionException:
        print("\n\nAn error occurred when establishing connection.\nCheck for Internet connection.")
        exit(8)
    except paramiko.ssh_exception.AuthenticationException:
        print("\n\nAuthentication failed.")
        exit(7)

    # Check for uploading directory
    print("Checking for %s... " % path, end='')
    if sftp.exists(path):
        print("Exist.")
        if fullsync:
            try:
                print("Removing %s... " % path, end='')
                sftp.execute("rm -rf %s" % path)
                print("Done.")
                print("Make directory at %s... " % path, end='')
                sftp.makedirs(path)
                print("Done.")
            except Exception as e:
                print("\nSFTP Error.")
                print(e)
                exit(9)
        else:
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
            if not lines:
                ignored = 0
            else:
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

                # If remote file does not exists
                if not sftp.exists(rpath):
                    print("Uploading: %s... " % rel, end='')
                    sftp.makedirs(os.path.dirname(rpath))
                    sftp.put(rel, remotepath=rpath, preserve_mtime=True)
                    print("Done.")
                    continue

                # Remote file exists
                # Gather information of remote file.
                fr = sftp.lstat(rpath)
                fl = os.stat(rel)

                # If remote file's modification time & size is the same as the
                # local one, stands the file is unchanged.
                if fr.st_size == fl.st_size and int(fr.st_mtime) == int(fl.st_mtime):
                    print("Skipped:   %s" % rel)
                else:
                    # Replace the remote one.
                    print("Uploading: %s... " % rel, end='')
                    try:
                        sftp.put(rel, remotepath=rpath, preserve_mtime=True)
                        print("Done.")
                    except Exception as e:
                        print('FAILED.')
                        print(e)

    # Close connection
    print("Disconnecting... ", end='')
    sftp.close()
    print("Done.")




if __name__ == '__main__':
    bootstrapper()
