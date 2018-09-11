"""
This is the agent application, runs silently in the background in the user's session
"""
import logging
from threading import Thread
from wsgiref.simple_server import make_server
from webapp.factory import create_app


def setup_logging():
    """
    Set up logging
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('log.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def main():
    """
    creates a new thread for the web server and starts it
    Waits for stop requested to stop the web server thread
    """
    logger = setup_logging()
    flask_app = create_app()
    server = make_server('0.0.0.0', 8002, flask_app)
    process = Thread(
        target=server.serve_forever)
    process.start()
    logger.info('Started Webserver on port 8002')

    running = True

    while 1:
        if running:
            # do work here.
            pass
        else:
            server.shutdown()
            process.join(timeout=2)
            logger.info('Shutting down webserver')
            break

if __name__ == '__main__':
    main()
