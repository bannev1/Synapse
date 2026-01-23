from app.models import Graph
from app.models.nodes import TopicNode


class CompareGraph(Graph):
	def __init__(self, graph1: Graph, graph2: Graph):
		"""
		Graph to compare two graphs
		"""

		# Set basic attributes
		query = f'{graph1.query} + {graph2.query}'
		type = f'{graph1.type} + {graph2.type}' if graph1.type != graph2.type else graph1.type # Either add types or change
		depth = max(graph1.depth, graph2.depth) # Max depth of both graphs
		sites = list(set(graph1.sites + graph2.sites)) # Non-duplicated combination of both graph sites

		self.graph1 = graph1
		self.graph2 = graph2

		super().__init__(query, type, depth, sites)

	

	def construct(self):
		"""
		Construct compare graph
		"""

		topics = {}

		# Create topic nodes
		for topic in (self.graph1.topicNodes + self.graph2.topicNodes):
			# If topic node already exists
			if topic.name in topics.keys():
				topics[topic.name].sourceNodes.extend(topic.sourceNodes)

			# Otherwise create node
			else:
				topicNode = TopicNode(topic.name, topic.sourceNodes)
				topics[topic.name] = topicNode

				self.topicNodes.append(topicNode)
