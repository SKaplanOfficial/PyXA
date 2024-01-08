class ApplicationNotFoundError(Exception):
    def __init__(self, name: str):
        self.name = name
        Exception.__init__(self, name)

    def __str__(self):
        return f"Application {self.name} not found."


class AuthenticationError(Exception):
    def __init__(self, message: str):
        self.message = message
        Exception.__init__(self, message)

    def __str__(self):
        return f"Failed due to insufficient authorization. {self.message}"


class InvalidPredicateError(Exception):
    def __init__(self, message: str):
        self.message = message
        Exception.__init__(self, message)

    def __str__(self):
        return f"Could not construct valid predicate format. {self.message}"


class UnconstructableClassError(Exception):
    def __init__(self, message: str):
        self.message = message
        Exception.__init__(self, message)

    def __str__(self):
        return f"Could not create new element. {self.message}"


class AppleScriptError(Exception):
    """Raised when an AppleScript error occurs."""

    def __init__(self, err: dict, script: str):
        error_number = err["NSAppleScriptErrorNumber"]
        error_message = err["NSAppleScriptErrorMessage"]
        error_range = err["NSAppleScriptErrorRange"].rangeValue()
        error_context = script[
            script.rfind("\n", 0, error_range.location) : script.find(
                "\n", error_range.location, len(script)
            )
        ].strip()

        print(script.split("\n"))
        error_line = next(
            (n for (n, l) in enumerate(script.split("\n")) if error_context in l), -1
        )

        self.number = int(error_number)
        self.message = error_message
        self.line_number = error_line
        self.near = error_context

        Exception.__init__(
            self,
            f"Error {self.number}: {self.message} On line #{self.line_number}: '{self.near}'.",
        )

    def __str__(self):
        return f"Error {self.number}: {self.message} On line #{self.line_number}: '{self.near}'."
