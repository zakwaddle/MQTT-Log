#!/bin/zsh

SOURCE_DIR="/Users/zakwaddle/MQTT-Log/MQTT-LogViewer/dist/"
DEST_DIR="zak@yawntsum.local:~/local_services/home-mqtt-log/log-viewer"
EXCLUDE_PATTERNS=('.idea/' 'node_modules/' 'app.js.LICENSE.txt' 'build/' 'public/' 'src/' 'sync.zsh' 'package.json' 'package-lock.json' 'zrc.js')

RSYNC_OPTIONS=(-avz)

for pattern in "${EXCLUDE_PATTERNS[@]}"
do
  RSYNC_OPTIONS+=("--exclude=$pattern")
done

rsync "${RSYNC_OPTIONS[@]}" "$SOURCE_DIR" "$DEST_DIR"
