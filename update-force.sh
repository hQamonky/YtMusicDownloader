#!/bin/bash

# Erase modifications (your database will be overwritten)
git -C ~/qmk/YtMusicDownloader reset --hard
# Update
~/qmk/YtMusicDownloader/update.sh

