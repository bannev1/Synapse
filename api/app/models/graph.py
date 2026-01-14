from typing_extensions import Literal

class Graph:
	def __init__(self, query: str, type: Literal['topical', 'medium', 'locational'], depth: int) -> None:
		"""
		Graph Base Class
		"""

		# Set attributes
		self.query: str = query
		self.type: Literal['topical', 'medium', 'locational'] = type
		self.depth: int = depth
