# Gekko
Make SFTP uploading "easy-peasy lizard squeezy".

## Uncompleted project, it's still under development.

## Installation
```
$ sudo apt-get update && sudo apt-get install -y python3 python3-pip
$ sudo pip3 isntall pysftp PyYAML
$ sudo wget --no-check-certificate https://raw.githubusercontent.com/CYRO4S/Gekko/master/gekko.py -O /usr/bin/gekko  
$ sudo chmod a+x /usr/bin/gekko
```
## Quick Start
Add files or directories you don't want to upload.  
```
$ gekko camo venv/
Checking for venv/... Exist.
/home/me/gekkotest/.gekkoign saved.
```  
Set up SFTP connection.
```
$ gekko grip root@myserver.com:/root/gekkotest-remote -s MyServer
Host:             myserver.com
SSH Port:         22
User:             root
Upload Directory: /root/gekkotest-remote
Remark:           MyServer

Connection Saved.
```
Set up SFTP connection using a rsa key and specify the ssh port.
```
$ gekko grip root@myserver.com:/root/gekkotest-remote -s MyServer -p 1080 -k ~/.ssh/id_rsa
Host:             myserver.com
SSH Port:         1080
User:             root
Upload Directory: /root/gekkotest-remote
Remark:           MyServer
Private key:      /home/ice/.ssh/id_rsa
```
Check for changes.  
```
$ gekko sense MyServer
Connecting to myserver.com... Connected.
Checking for changes... Done.
Local                       Remote
-----                       -----
app/main/views.py           + app/main/views.py
app/templates/index.html    + app/templates/index.html
requirements.txt            + requirements.txt
manager.py                  * manager.py
                            - README.md
```
Upload using password.
```
$ gekko run MyServer -p P@ssw0rd
Connecting to myserver.com... Connected.
Make directory at /root/gekkotest-remote... Skipped.
Change directory to /root/gekkotest-remote... Done.
Ignored:   .gekkoign
Uploading: app/main/views.py... Done.
Uploading: app/templates/index.html... Done.
Skipped:   app/templates/old.html
Ignored:   venv/lib/python3.5/site.py
......
Ignored:   venv/pip-selfcheck.json
Skipped:   oldone.txt
Uploading: requirements.txt... Done.
Uploading: manager.py... Done.
Disconnecting... Done.

Operation successfully completed.
```

## Commands

* camouflage (camo)   : Define a file or a directory which will be ignored when uploading. This will generate '.gekkoign' file.
* grip (gp)           : Create a host which files will be uploaded to. You can also save the host or remove it.
* list (ls)           : Show all the connections.
* remove (rm)         : Remove a connecion.
* run (rn)            : Start the upload sequence.
