# Gekko
Make SFTP upload "easy-peasy lizard squeezy".

## Uncompleted project, it's still under development.

## Quick Start
Add files or directories you don't want to upload.  
```
$ gekko camo venv/
Checking for venv/... Exist.
/home/me/gekkotest/.gekkoign saved.
```  
Set up SFTP connection.
```
$ gekko grip root@myserver.com:22#/root/gekkotest-remote -s MyServer
Host:             myserver.com
SSH Port:         22
Upload Directory: /root/gekkotest-remote
Remark:           MyServer

Connection Saved.
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
$ gekko run MyServer
Connecting to myserver.com... Connected.
Checking for changes... Done.
Uploading app/main/views.py... Done.
Uploading app/templates/index.html... Done.
Uploading requirements.txt... Done
Removing manager.py... Done.
Uploading manager.py... Done.
Removing README.md... Done.

All done.
```
