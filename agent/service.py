"""
This module is responsible for being the entry point for the installation
of the service and the starting of the service managers internally
Starts the web service also
This is the server version
"""
import sys
import time
import socket
import logging
import multiprocessing
import win32serviceutil
from gevent.pywsgi import WSGIServer
import win32service
import win32event
import servicemanager
from webapp.factory import create_app


def setup_logging():
    """
    Set up logging
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('C:\\clear\\log.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

class WebServer(multiprocessing.Process):
    """
    class for controlling web server process
    """
    def __init__(self, ):
        """
        create process and exit event ready
        """
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('C:\\clear\\webserver.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def run(self):
        """
        run the web server
        """
        while not self.exit.is_set():
            flask_app = create_app()
            host = '0.0.0.0' # listen on all addresses
            port = 8003

            app_server = WSGIServer((host, port), flask_app, keyfile='agent.key',
                                    certfile='agent.crt')
            app_server.serve_forever()

    def shutdown(self):
        """
        callback to shutdown the web server process
        """
        self.exit.set()



class AppServerSvc(win32serviceutil.ServiceFramework):
    """
    Main class which allows controlling the service from Windows
    """
    _svc_name_ = "SELAgent-Agent"
    _svc_display_name_ = "SELAgent Agent"

    def __init__(self, args):
        """
        Create the new service, create new event stating service is starting
        """
        self.logger = setup_logging()
        self.logger.info('hello')
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.h_waitstop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        """
        Callback for when a stop is requested, the loops look at this to
        determine when to close themselves
        """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.h_waitstop)
        self.stop_requested = True

    def SvcDoRun(self):
        """
        Log message telling service manager that the service has started
        and start the main function which starts everything else
        """
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.main()

    def main(self):
        """
        Creates a worker in a separate process to start the web server in
        Also waits for a stop to be requested to kill the processes
        """
        process = WebServer()
        process.start()
        while 1:
            time.sleep(2)
            if self.stop_requested:
                self.logger.info('shutting down')
                process.terminate()
                process.join()
                return


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AppServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)
