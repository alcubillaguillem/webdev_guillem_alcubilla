"""Domain errors. Services raise them; routes turn them into status codes."""


class DomainError(Exception):
    status = 400

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class NotAuthenticated(DomainError):
    status = 401


class InvalidCredentials(DomainError):
    status = 401
