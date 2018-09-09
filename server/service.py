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
from threading import Thread
from wsgiref.simple_server import make_server
import win32serviceutil
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


class AppServerSvc(win32serviceutil.ServiceFramework):
    """
    Main class which allows controlling the service from Windows
    """
    _svc_name_ = "SELAgent-Server"
    _svc_display_name_ = "SELAgent Server"

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
        creates a new thread for the web server and starts it
        Waits for stop requested to stop the web server thread
        """
        flask_app = create_app()
        server = make_server('localhost', 8002, flask_app)
        process = Thread(
            target=server.serve_forever)
        process.start()

        # start service loop
        while 1:
            time.sleep(2)
            if self.stop_requested:
                server.shutdown()
                process.join(timeout=2)
                break



if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AppServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)
