import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def loggerSetup(name, logFile, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(logFile)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger