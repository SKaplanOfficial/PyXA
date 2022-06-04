class ApplicationNotFoundError(Exception):
	def __init__(self, name):
		self.name = name
		Exception.__init__(self, name)
	
	def __str__(self):
		return f'Application {self.name} not found.'