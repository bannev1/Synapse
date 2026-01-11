from app.models.nodes.node import Node


class GraphNode(Node):
	def __init__(self, 
			  	name: str, 
				color: list[int], 
				titleNode: 'TitleNode', 
				depth: int, 
				sources: list[str]
			) -> None:
		
		# Save attributes of inherited function
		super(Node, self).__init__(name, color)

		# Define attributes for GraphNode
		self.titleNode: 'TitleNode' = titleNode
		self.depth: int = depth
		self.sources: list[str] = sources
