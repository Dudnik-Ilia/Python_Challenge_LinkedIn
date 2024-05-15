from termcolor import colored


class ScribeException(Exception):
    def __init__(self, message: str):
        super().__init__(colored(message, 'red'))

class InvalidInputException(ScribeException):
    pass