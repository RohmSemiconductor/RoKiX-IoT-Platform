# 
# Copyright 2020 Rohm Semiconductor
#
class EvaluationKitException(Exception):
    pass


class FunctionalityNotInDevice(EvaluationKitException):
    pass


class ProtocolException(EvaluationKitException):
    """Exception for protocol-related issues.

    Args:
        msg (str, optional): a free-form message; shown in tracebacks
        status (int, optional): protocol status code
    """

    def __init__(self, msg='', status=None):
        EvaluationKitException.__init__(self, msg)
        self.status = status


class ProtocolTimeoutException(ProtocolException):
    pass


class ProtocolBus1Exception(ProtocolException):
    pass


class ProtocolBus2Exception(ProtocolException):
    pass
