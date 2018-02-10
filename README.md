# Gekko
Make SFTP uploading "easy-peasy lizard squeezy".

## Uncompleted project, it's still under development.

## Installation
```
$ sudo apt-get update && sudo apt-get install -y python3 python3-pip
$ sudo pip3 isntall pysftp 
# download pyyaml
$ curl -sL https://github.com/yaml/pyyaml/archive/3.12.tar.gz > pyyaml-3.12.tar.gz
$ tar vxf pyyaml-3.12.tar.gz
$ cd pyyaml-3.12
#install pyyaml. refer to http://pyyaml.org/wiki/PyYAMLDocumentation
$ sudo python3 setup.py install

#TODO install gekko

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
$ gekko make root@myserver.com:/root/gekkotest-remote -s MyServer
Host:             myserver.com
SSH Port:         22
User:             root
Upload Directory: /root/gekkotest-remote
Remark:           MyServer

Connection Saved.
```
Set up SFTP connection using a rsa key and specify the ssh port.
```
$ gekko make root@myserver.com:/root/gekkotest-remote -s MyServer -p 1080 -k ~/.ssh/id_rsa
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
Finally, commit upload.  
```
$ gekko upload MyServer -p P@aaw0rd
Connecting to myserver.com... Connected.
Make directory at /root/gekkotest-remote... Skipped.
Change directory to /root/gekkotest-remote... Done.
Ignored:   .gekkoign
Uploading: app/main/views.py... Done.
Uploading: app/templates/index.html... Done.
Ignored:   venv/lib/python3.5/site.py
......
Ignored:   venv/pip-selfcheck.json
Uploading: requirements.txt... Done.
Uploading: manager.py... Done.
Disconnecting... Done.

Operation successfully completed.
```
Upload using password.
```
$ gekko upload MyServer -p P@aaw0rd
Connecting to myserver.com... Connected.
Make directory at /root/gekkotest-remote... Skipped.
Change directory to /root/gekkotest-remote... Done.
Ignored:   .gekkoign
Uploading: app/main/views.py... Done.
Uploading: app/templates/index.html... Done.
Ignored:   venv/lib/python3.5/site.py
......
Ignored:   venv/pip-selfcheck.json
Uploading: requirements.txt... Done.
Uploading: manager.py... Done.
Disconnecting... Done.

Operation successfully completed.
```

## Commands

* camouflage (camo)   : Define a file or a directory which will be ignored when uploading. This will generate '.gekkoign' file.
* make (mk)           : Create a host which files will be uploaded to. You can also save the host or remove it
* list (ls)           : Show all the connections.
* remove (rm)         : Remove a connecion.
* upload (ul)         : Start the upload sequence.
