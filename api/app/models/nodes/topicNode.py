from app.models.nodes.node import Node
from app.models.nodes.sourceNode import SourceNode


class TopicNode(Node):
	def __init__(self, 
			  	name: str,
				sourceNodes: list[SourceNode]
			) -> None:
		
		# Save attributes of inherited function
		super(Node, self).__init__(name)

		# Set own attributes
		self.sourceNodes: list[SourceNode] = sourceNodes
