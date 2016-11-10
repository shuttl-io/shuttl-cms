SHUTTL_DIR=$HOME/.shuttl/

shuttl() {
    if test "$1" == "launch"
    then
        sh $SHUTTL_DIR/run.sh 
        return
    fi
    if test "$1" == "update"
    then
        sh $SHUTTL_DIR/update.sh 
        return
    fi
    source $SHUTTL_DIR/shuttlVenv/bin/activate
    python $SHUTTL_DIR/run.py $*
    deactivate
}
