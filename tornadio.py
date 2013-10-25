#!/user/bin/python env
import logging

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.dirname(__file__)+"/pongserver")
    print sys.path
    from pongserver import settings
    logging.debug('All set up !')
    from pongserver.tornadio.server import application
    sys.exit(application())
