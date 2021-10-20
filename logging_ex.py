import logging


def getLogger(name, fmt="[%(asctime)s]%(name)s<%(levelname)s>%(message)s",
              terminator='\n'):
    logger = logging.getLogger(name)
    cHandle = logging.StreamHandler()
    cHandle.terminator = terminator
    cHandle.setFormatter(logging.Formatter(fmt=fmt, datefmt="%H:%M:%S"))
    logger.addHandler(cHandle)
    return logger


logger = getLogger(r'\n', terminator='\n')
rlogger = getLogger(r'\r', terminator='\r')

logger.setLevel(logging.DEBUG)
rlogger.setLevel(logging.DEBUG)


logger.info('test0')
logger.info('test1')
logger.info('-----------------------\n')
rlogger.info('test2')
rlogger.info('test3\n\n')

for i in range(100000):
    rlogger.info("%d/%d", i + 1, 100000)
rlogger.info('\n')