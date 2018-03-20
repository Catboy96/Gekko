<p align="center">
  <img src="https://raw.githubusercontent.com/CYRO4S/Gekko/master/assets/gekko_icon.png" width="132" height="132" alt="Gekko_LOGO">
  <img src="https://raw.githubusercontent.com/CYRO4S/Gekko/master/assets/gekko_text.png" alt="Gekko">
  <br />
</p>

<p align="center">A command line tool makes SFTP sync "easy-peasy lizard-squeezy".<br /></p>
  
[![PyPI version](https://badge.fury.io/py/theGekko.svg)](https://badge.fury.io/py/theGekko)  

## Contents  
* [Installation](#installation)  
* [Enable tab-complete](#enable-tab-complete)
* [Quick start](#quick-start)
* [Commands list](#commands)
* [Detailed Wiki (中文 / English)](https://github.com/CYRO4S/Gekko/wiki)

## Installation
```shell
$ sudo apt-get update && sudo apt-get install -y python3 python3-pip
$ sudo pip3 install thegekko
```
## Enable tab-complete  
Add the content of [tab-complete/gekko_tc](https://github.com/CYRO4S/Gekko/blob/master/tab-complete/gekko_tc) to ~/.bashrc. Then,  
```shell
$ source ~/.bashrc
```
## Quick Start
Add files or directories you don't want to sync.  
```shell
$ gekko camo venv/
Checking for venv/... Exist.
/home/me/gekkotest/.gekkoign saved.
```  
Set up SFTP connection.
```shell
$ gekko grip root@myserver.com:/root/gekkotest-remote -s MyServer
Host:             myserver.com
SSH Port:         22
User:             root
Upload Directory: /root/gekkotest-remote
Remark:           MyServer

Connection Saved.
```
Set up SFTP connection using a rsa key and specify the ssh port.
```shell
$ gekko grip root@myserver.com:/root/gekkotest-remote -s MyServer -p 1080 -k ~/.ssh/id_rsa
Host:             myserver.com
SSH Port:         1080
User:             root
Upload Directory: /root/gekkotest-remote
Remark:           MyServer
Private key:      /home/ice/.ssh/id_rsa
```
Check for changes.  
```shell
$ gekko sense MyServer -p P@ssw0rd
Connecting to myserver.com... Connected.
Checking for /root/gekkotest-remote... Exist.
Changes will be taken:
* /root/gekkotest-remote/app.py
+ /root/gekkotest-remote/assets/logo.png
Disconnecting... Done.

0.102 MB need to upload.
```
Sync using password. Add ```-f``` if you want to a full sync.  
Full sync will erase remote folder and re-upload local files.  
```shell
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
Reserved:  db.py
Disconnecting... Done.
```

## Commands

* camouflage (camo)   : Define a file or a directory which will be ignored when uploading. This will generate '.gekkoign' file.
* grip (gp)           : Create a host which files will be uploaded to. You can also save the host or remove it.
* list (ls)           : Show all the connections.
* remove (rm)         : Remove a connecion.
* sense (ss)          : Check for the changes which will taken in uploading.
* run (rn)            : Start the upload sequence.
* version (ver)       : Show Gekko version.
