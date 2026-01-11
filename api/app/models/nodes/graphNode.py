from app.models.nodes import Node

class GraphNode(Node):
	def __init__(self, 
			  	name: str, 
				color: list[int], 
				neighbors: list[Node], 
				titleNode: 'TitleNode', 
				depth: int, 
				sources: list[str]
			) -> None:
		
		# Save attributes of inherited function
		super(Node, self).__init__(name, color, neighbors)

		# Define attributes for GraphNode
		self.titleNode = titleNode
		self.depth = depth
		self.sources = sources
