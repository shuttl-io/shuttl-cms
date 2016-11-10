#!/bin/bash
CUR_DIR=$(pwd)
SHUTTL_PATH=$HOME/.shuttl/
cd $SHUTTL_PATH
. shuttlVenv/bin/activate
export PYTHONPATH="$SHUTTL_PATH:$PYTHONPATH"
python daemons/PublishWorker.py start
python run.py runserver
python daemons/PublishWorker.py stop
cd $CUR_DIR
