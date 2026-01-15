from app.models.nodes.node import Node


class SourceNode(Node):
	def __init__(self, 
			  	name: str,
				source: str,
				query: str, 
				medium: str,
				location: str,
				topics: list[str] | None = None,
				neighbors: list['SourceNode'] | None = None
			) -> None:
		
		# Save attributes of inherited function
		super(Node, self).__init__(name)

		# Define attributes for SourceNode
		self.source: str = source
		self.query: str = query
		self.topics: list[str] | None = topics
		self.medium: str = medium
		self.location: str = location

		# Define attributes for links
		self.neighbors: list['SourceNode'] | None = neighbors

	
	# For conversion of dictionary
	def keys(self):
		"""
		Return the keys of the dictionary
		"""
		yield ['source', 'name', 'topics', 'medium', 'location', 'neighbors']


	def __getitem__(self, key: str):
		"""
		Return an item/value for a key
		"""

		match key:
			case 'source':
				return self.source
			case 'name':
				return self.query
			case 'topics':
				return self.topics
			case 'medium':
				return self.medium
			case 'location':
				return self.location
			case 'neighbors':
				return [node.source for node in self.neighbors]
