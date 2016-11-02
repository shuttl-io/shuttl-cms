import os
import sys

from base import Daemon
from shuttl import app
from shuttl.Models.Queue import Queue
from shuttl.Models.Website import Website


## A worker daemon that clears out the publish Queue. This checks the Queue to 
# see if there are any publish messages in there, if there is, publish them
# else ignore. 
# \note right now this works by constantly polling the DB to see if there is a 
# task. It would be graet if we could redesign this to be a monitor or semaphore
# of some type.
class PublishWorker(Daemon):

    ## This is continuously running. This is what clears out the  queue. This 
    # constantly checks to see if there is something in the database
     def run(self):
        print("Publisher Has started")
        with app.app_context():
            while True:
                kwargs = {}
                if not Queue.Empty():
                    obj = Queue.Pop()
                    try:
                        print ("publishing the websites")
                        if type(obj) == Website:
                            kwargs = {"website": obj}
                            obj.publish()
                            pass
                        else:
                            kwargs = {"fileObject": obj}
                            site = obj.website
                            site.publish(obj)
                            pass
                        pass
                    except Exception as e:
                        import logging
                        args = [
                            type(obj), 
                            obj.id,
                            obj.name
                        ]
                        logging.exception(
                            "An Error prevented publishing! the type is {0}, the id {1} and the name is {2}".format(*args)
                        )
                        entry = Queue.Push(**kwargs)
                        entry.recoverable = False
                        entry.save()
                        pass
                    pass
                pass
            pass
        pass
    
## \cond
if __name__ == "__main__":
    daemon = PublishWorker(
        os.path.join(app.config["PID_PATH"], "publish.pid"),
        stdout=os.path.join(app.config["LOG_PATH"], "publish.log"), 
        stderr=os.path.join(app.config["LOG_PATH"], "publish.error") 
    )
    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                    daemon.start()
            elif 'stop' == sys.argv[1]:
                    daemon.stop()
            elif 'restart' == sys.argv[1]:
                    daemon.restart()
            else:
                    print( "Unknown command")
                    sys.exit(2)
            sys.exit(0)
    else:
            print ("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)
## \endcond