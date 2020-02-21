# Directory Organizer
This script be able you to organize your "Download" directory.

# Requiriments
- Python3 or Higher
- pip3

# Install 
```
pip install -r requirements.txt
```

# Deploy (Linux)
with cron:
```
sudo crontab -e 
```
add at crontab file in the last line:
```
@reboot sleep 30 & python3 /REPO_PATH/main.py
```
after that, reboot your system, and see!

# Deploy (Windows)
In the glorious Windows is more complex, therefore you need this tutorial:
[Tutorial in Medium](https://www.google.com)

