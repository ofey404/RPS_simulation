#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

date_str=$(date +%Y-%m-%d-%H:%M:%S)

mkdir -p $SCRIPT_DIR/data/$date_str
cp $SCRIPT_DIR/template/config.json $SCRIPT_DIR/data/$date_str/config.json

vim $SCRIPT_DIR/data/$date_str/config.json

python $SCRIPT_DIR/main.py $SCRIPT_DIR/data/$date_str/config.json
python $SCRIPT_DIR/plot.py $SCRIPT_DIR/data/$date_str/config.json

xdg-open $SCRIPT_DIR/data/$date_str/

