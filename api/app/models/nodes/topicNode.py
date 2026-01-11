from app.models.nodes.node import Node


class TopicNode(Node):
	def __init__(self, 
			  	name: str, 
				color: list[int], 
				neighbors: list[Node]
			) -> None:
		
		# Save attributes of inherited function
		super(Node, self).__init__(name, color, neighbors)
