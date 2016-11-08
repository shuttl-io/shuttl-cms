#!/bin/bash
CUR_DIR=$(pwd)

cd $HOME/.shuttl/

source shuttlVenv/bin/activate

python daemons/PublishWorker.py start
python run.py runserver
python daemons/PublishWorker.py stop
cd $CUR_DIR