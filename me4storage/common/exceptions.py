class RegexError(Exception):
    pass

class UsageError(Exception):
    pass

class UnknownError(Exception):
    pass

class LoginError(Exception):
    pass

class ApiError(Exception):
    pass

class NotFoundError(Exception):
    pass

class IncompleteResponseError(ApiError):

    def __init__(self, msg):

        super().__init__(
            f"This library was expecting a value that is missing from "
            f"the response ({msg}). Possibly the API has changed it's "
            f"response format."
        )
