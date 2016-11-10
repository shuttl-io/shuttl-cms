#!/bin/bash
CUR_DIR=$(pwd)
SHUTTL_DIR=$HOME/.shuttl
git clone https://github.com/shuttl-io/shuttl.git $SHUTTL_DIR
cd $SHUTTL_DIR
mkdir -p media/{templates,css,js,generic}
pip install virtualenv
virtualenv --python=$(which python3) shuttlVenv
source shuttlVenv/bin/activate
pip install -r requirements.txt
python run.py db init
python run.py db migrate
python run.py db upgrade
cd $SHUTTL_DIR/shuttl/static/
npm install
npm run build
npm run buildInternal
cd sass
sass style.scss:$SHUTTL_DIR/shuttl/static/css/style.css
sudo sh -c "echo '127.0.0.1       shuttl.local' >> /etc/hosts"
echo $(pwd)
cd $SHUTTL_DIR
python run.py filldb
read -t 1 -n 10000000 discard 
python run.py add --organization shuttl
echo "Default organization is shuttl. run run.sh and then go to shuttl.shuttl.local"
echo "source $SHUTTL_DIR/functions.sh" >> $HOME/.bash_profile 
source $HOME/.bash_profile
cd $CUR_DIR
