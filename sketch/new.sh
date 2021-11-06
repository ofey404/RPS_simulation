#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# NOTICE: Change to what you like!
EDITOR=vim
FILE_MANAGER=xdg-open

date_str=$(date +%Y-%m-%d-%H:%M:%S)

mkdir -p $SCRIPT_DIR/data/$date_str
cp $SCRIPT_DIR/template/config.json $SCRIPT_DIR/data/$date_str/config.json

$EDITOR $SCRIPT_DIR/data/$date_str/config.json

python $SCRIPT_DIR/main.py $SCRIPT_DIR/data/$date_str/config.json
python $SCRIPT_DIR/plot.py $SCRIPT_DIR/data/$date_str/config.json

$FILE_MANAGER $SCRIPT_DIR/data/$date_str/

