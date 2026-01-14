from app.models.nodes.node import Node


class SourceNode(Node):
	def __init__(self, 
			  	name: str, 
				color: list[int], 
				query: str, 
				topics: list[str],
				mediums: list[str],
				location: str,
				neighbors: list['SourceNode']
			) -> None:
		
		# Save attributes of inherited function
		super(Node, self).__init__(name, color)

		# Define attributes for SourceNode
		self.query: str = query
		self.topics: list[str] = topics
		self.mediums: list[str] = mediums
		self.location: str = location

		# Define attributes for links
		self.neighbors: list['SourceNode'] = neighbors
