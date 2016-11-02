## 
# \file backend_scripts/daemonbase.py
# \author Yoseph Radding
#
# Defines the base class for Python Deamons.

import sys, os, time, atexit
from signal import SIGTERM

## Defines the Daemon base class
#
# \note \par Subclassing
# This class should be subclased. The only thing that needs to be overrided is the run function.
class Daemon:
        """
        A generic daemon class.
       
        Usage: subclass the Daemon class and override the run() method
        """

        ## Initializes the deamon
        # \param pidfile the file containing the PID
        # \param stdin the stdin for the deamon
        # \param stdout the stdout for the deamon 
        # \param stderr the stderr for the deamon 
        def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):

                ## the stdin
                self.stdin = stdin

                ## the stdout
                self.stdout = stdout

                ## the stderr
                self.stderr = stderr

                ## the pid file
                self.pidfile = pidfile
       
        ##do the UNIX double-fork magic, see Stevens' "Advanced Programming in 
        # the UNIX Environment" for details (ISBN 0201563177) 
        # http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        def daemonize(self):
                """
                do the UNIX double-fork magic, see Stevens' "Advanced
                Programming in the UNIX Environment" for details (ISBN 0201563177)
                http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
                """
                try:
                        pid = os.fork()
                        if pid > 0:
                                # exit first parent
                                sys.exit(0)
                except OSError as e:
                        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
       
                # decouple from parent environment
                os.chdir("/")
                os.setsid()
                os.umask(0)
       
                # do second fork
                try:
                        pid = os.fork()
                        if pid > 0:
                                # exit from second parent
                                sys.exit(0)
                except OSError as e:
                        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
       
                # redirect standard file descriptors
                sys.stdout.flush()
                sys.stderr.flush()

                ## Actual file for stdin
                self.si = open(self.stdin, 'r')

                ## Actual file for stdout
                self.so = open(self.stdout, 'a+')

                ## Actual  file for stderr
                self.se = open(self.stderr, 'a+')
                os.dup2(self.si.fileno(), sys.stdin.fileno())
                os.dup2(self.so.fileno(), sys.stdout.fileno())
                os.dup2(self.se.fileno(), sys.stderr.fileno())
       
                # write pidfile
                atexit.register(self.delpid)
                pid = str(os.getpid())
                open(self.pidfile,'w+').write("%s\n" % pid)
       
        ## Deletes the pid file
        #
        def delpid(self):
                os.remove(self.pidfile)
 
        ## Start the Deamon
        def start(self):
                """
                Start the daemon
                """
                # Check for a pidfile to see if the daemon already runs
                try:
                        pf = open(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
       
                if pid:
                        message = "pidfile %s already exist. Daemon already running?\n"
                        sys.stderr.write(message % self.pidfile)
                        sys.exit(1)
               
                # Start the daemon
                self.daemonize()
                self.run()
        
        ## stop the deamon
        def stop(self):
                """
                Stop the daemon
                """
                # Get the pid from the pidfile
                try:
                        pf = open(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
       
                if not pid:
                        message = "pidfile %s does not exist. Daemon not running?\n"
                        sys.stderr.write(message % self.pidfile)
                        return # not an error in a restart
 
                # Try killing the daemon process       
                try:
                        while 1:
                                os.kill(pid, SIGTERM)
                                time.sleep(0.1)
                except OSError as err:
                        err = str(err)
                        if err.find("No such process") > 0:
                                if os.path.exists(self.pidfile):
                                        os.remove(self.pidfile)
                        else:
                                print (str(err))
                                sys.exit(1)
        ## Just call stop and start
        def restart(self):
                """
                Restart the daemon
                """
                self.stop()
                self.start()
        
        ## Run the deamon override this in subclass
        def run(self):
                """
                You should override this method when you subclass Daemon. It will be called after the process has been
                daemonized by start() or restart().
                """
                raise NotImplemented("Run is not implement in {0}".format(self.__class__.__name__))

