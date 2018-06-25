class I2CError(Exception):
    """Base class for errors raised by I2C."""


class InitError(I2CError):
    """Exception raised for initialization errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message, logger=None):
        self.message = message
        if logger != None:
            logger.error(message)


class ReadError(I2CError):
    """Exception raised for read errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message, logger=None):
        self.message = message
        if logger != None:
            logger.error(message)


class WriteError(I2CError):
    """Exception raised for write errors.

    Attributes:
        message -- explanation of the error
        byte_list -- TODO
    """

    def __init__(self, message, logger=None):
        self.message = message
        if logger != None:
            logger.error(message)


class MuxError(I2CError):
    """Exception raised for write errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message, logger=None):
        self.message = message
        if logger != None:
            logger.error(message)
