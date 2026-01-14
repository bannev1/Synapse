from app.models.nodes.node import Node


class SourceNode(Node):
	def __init__(self, 
			  	name: str,
				source: str,
				query: str, 
				topics: list[str],
				medium: str,
				location: str,
				neighbors: list['SourceNode'] = []
			) -> None:
		
		# Save attributes of inherited function
		super(Node, self).__init__(name)

		# Define attributes for SourceNode
		self.source: str = source
		self.query: str = query
		self.topics: list[str] = topics
		self.medium: str = medium
		self.location: str = location

		# Define attributes for links
		self.neighbors: list['SourceNode'] = neighbors
