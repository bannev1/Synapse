from app.models.nodes.node import Node


class SourceNode(Node):
	def __init__(self, 
			  	name: str, # Website Title
				source: str, # Website URL
				sourceName: str, # Website Creator Title
				query: str, 
				medium: str,
				location: str,
				topics: list[str] | None = None,
				neighbors: list['SourceNode'] | None = None
			) -> None:
		
		# Save attributes of inherited function
		super().__init__(name)

		# Define attributes for SourceNode
		self.source: str = source
		self.sourceName: str = sourceName
		self.query: str = query
		self.topics: list[str] | None = topics
		self.medium: str = medium
		self.location: str = location

		# Define attributes for links
		self.neighbors: list['SourceNode'] | None = neighbors

	

	def toDict(self):
		"""
		Convert this node to dictionary
		"""

		return {
			'source': self.source, 
			'name': self.name, 
			'sourceName': self.sourceName,
			'topics': self.topics, 
			'medium': self.medium, 
			'location': self.location, 

			# Convert neighbors to string
			'neighbors': [node.source for node in self.neighbors]
		}
