# Directory Organizer
This script let you organize your "Download" directory or another that you want to organize.

![demo](https://github.com/cr0wg4n/directory-organizer/blob/master/img/demo_gif.gif)
![demo2](https://github.com/cr0wg4n/directory-organizer/blob/master/img/demo_pdfs.gif)

Link to project description in [Medium](https://medium.com/@cr0wg4n/automatizando-tareas-aburridas-con-python-organizador-de-directorios-7ed9b6a4dfe)

## Requiriments
- Python3 or Higher
- pip3

## Install 
```
pip install -r requirements.txt
```

In main.py file, you must modify the PATH variable, with your Download directory path, for example:

```
PATH = "D:/Descargas/"
```
Is important keep `/` if your path is more large, for example:
```
C:/example/example/example/example/
```
and `/` at the end.

## Deploy (Linux)
with cron:
```bash
sudo crontab -e 
```
in the cron file add this line at the end:
```
@reboot sleep 30 & python3 /REPO_ABSOLUTE_PATH/main.py
```
reload the cron service:
```
sudo service cron  reload
sudo service cron restart
```
after that, reboot your system, and see!

## Deploy (Windows)
In the glorious Windows is a little bit more easier, edit the `run_with_windows.bat` file and put your path, in this 
case we use `pythonw.exe` of my virtual enviroment for run this file in background, the real path of `pythonw.exe` in many cases is `C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python37-32\pythonw.exe`.

After that, make a shortcut of `run_with_windows.bat` and move it to startup folder of Windows, you find this folder with
WIN+R (keys) and typing `shell:startup`. Reboot your system, and see (probably you find a terminal at the boot, if you want close it).
