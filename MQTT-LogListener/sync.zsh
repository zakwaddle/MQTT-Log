#!/bin/zsh

SOURCE_DIR="/Users/zakwaddle/MQTT-Log/MQTT-LogListener/"
DEST_DIR="zak@yawntsum.local:~/local_services/home-mqtt-log/log-listener/"
EXCLUDE_PATTERNS=('.idea/' '__pycache__/' 'venv/' 'sync.zsh' '.DS_Store' '.env')

RSYNC_OPTIONS=(-avz)

for pattern in "${EXCLUDE_PATTERNS[@]}"
do
  RSYNC_OPTIONS+=("--exclude=$pattern")
done

rsync "${RSYNC_OPTIONS[@]}" "$SOURCE_DIR" "$DEST_DIR"
