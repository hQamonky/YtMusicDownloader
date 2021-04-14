#!/bin/bash

# Update
git -C ~/qmk/YtMusicDownloader pull
# Set permissions
chmod +x ~/qmk/YtMusicDownloader/run.sh
chmod +x ~/qmk/YtMusicDownloader/update.sh
chmod +x ~/qmk/YtMusicDownloader/update-force.sh
# Restart service
sudo systemctl restart qmk_ymd

