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