from app.models.nodes.node import Node


class TitleNode(Node):
	def __init__(self, 
			  	name: str, 
				color: list[int],
				topicNodes: list['TopicNode']
			) -> None:
		
		# Save attributes of inherited function
		super(Node, self).__init__(name, color)

		# Define attributes for SourceNode
		self.topicNodes: list['TopicNode'] = topicNodes
