#!/bin/bash

CUR_DIR=$(pwd)

SHUTTL_DIR=$HOME/.shuttl

git clone https://github.com/shuttl-io/shuttl.git $SHUTTL_DIR
cd $SHUTTL_DIR

pip install virtualenv
virtualenv --python=$(which python3) shuttlVenv
source shuttlVenv/bin/activate

pip install -r requirements.txt

python run.py db init
python run.py db migrate
python run.py db upgrade

cd shuttl/static/

npm install
npm run build
npm run buildInternal

sudo sh -c "echo '127.0.0.1       shuttl.local' >> /etc/hosts"
echo $(pwd)
python run.py add --organization shuttl
sudo sh -c "echo '127.0.0.1       shuttl.shuttl.local' >> /etc/hosts"
echo "Default organization is shuttl. run run.sh and then go to shuttl.shuttl.local"
echo "source $SHUTTL_DIR/functions.sh" >> $HOME/.bash_profile 
source $HOME/.bash_profile

cd $CUR_DIR