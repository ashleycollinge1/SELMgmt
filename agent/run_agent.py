"""
This is the agent application, runs silently in the background in the user's session
"""
import os
import logging
import itertools
import glob
from threading import Thread
from wsgiref.simple_server import make_server
from webapp.factory import create_app
from utilities.graphical import SysTrayIcon


def setup_logging():
    """
    Set up logging
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        os.mkdir('{}\\SELAgent'.format(os.getenv('APPDATA')))
    except WindowsError:
        pass
    file_handler = logging.FileHandler('{}\\SELAgent\\log.log'.format(os.getenv('APPDATA')))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def main():
    """
    creates a new thread for the web server and starts it
    Waits for stop requested to stop the web server thread
    Also creates the systray aspect of the agent software
    """
    logger = setup_logging()
    flask_app = create_app()
    server = make_server('0.0.0.0', 8002, flask_app)
    process = Thread(
        target=server.serve_forever)
    process.start()
    logger.info('Started Webserver on port 8002')

    icons = 'connected.ico'
    hover_text = 'SELAgent'

    def hello(var):
        """
        The hello test function
        """
        print "Hello world."

    menu_options = (('About', None, hello),
                    ('Switch Icon', None, hello),
                    ('Tools', None, (('Example1', None, hello),
                                     ('Example2', None, hello))))
    def bye(var):
        """
        Callback from when the application is requested to quit
        """
        server.shutdown()
        process.join(timeout=2)
        logger.info('Shutting down webserver')

    SysTrayIcon(icons, hover_text, menu_options, on_quit=bye, default_menu_index=1)

if __name__ == '__main__':
    main()
