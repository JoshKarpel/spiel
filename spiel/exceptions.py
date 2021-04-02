class SpielException(Exception):
    pass


class DuplicateInputHandler(SpielException):
    pass


class UnknownModeError(SpielException):
    pass


class NoDeckFound(SpielException):
    pass


class Quit(SpielException):
    pass
