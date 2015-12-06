# move_torrents.py

Have you just renamed a directory or moved your storage to a new hard-drive and now all of your torrents need to be updated?

This script only works on qBittorrent 3.3+ because in that version the location for torrent metadata was moved.

### example usage

```
# Backup the BT_BACKUP directory, in case something goes wrong.
$ cp -r "C:\\Users\\Jimi\\AppData\\Local\\qBittorrent\\BT_BACKUP" "C:\\Users\\Jimi\\AppData\\Local\\qBittorrent\\BT_BACKUP_2"

# Install the script's dependencies.
$ pip install requirements.txt

# Run the script with the three required arguments.
$ python move_torrents.py --find-path "F:\\Anime\\" --replace-path "F:\\" --bt-backup-path "C:\\Users\\Jimi\\AppData\\Local\\qBittorrent\\BT_BACKUP"
```
