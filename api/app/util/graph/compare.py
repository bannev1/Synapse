from app.models import Graph
from app.models.nodes import TopicNode


class CompareGraph(Graph):
	def __init__(self, graph1: dict, graph2: dict) -> None:
		"""
		Graph to compare two graphs (graphs given in JSON/dict format)
		"""

		# Set basic attributes
		query = f'{graph1["name"]} + {graph2["name"]}'
		type = f'{graph1["type"]} + {graph2["type"]}' if graph1["type"] != graph2["type"] else graph1["type"] # Either add types or change
		depth = max(graph1["depth"], graph2["depth"]) # Max depth of both graphs

		graph1Sites = [i['source'] for i in graph1['sources']]
		graph2Sites = [i['source'] for i in graph2['sources']]

		sites = list(set(graph1Sites + graph2Sites)) # Non-duplicated combination of both graph sites

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


		# Merge duplicate sourceNodes
		for source, node in (self.graph1.sources.items() + self.graph2.sources.items()):
			# If found duplicate
			if source in self.sources.keys():
				dupliNode = self.sources[source]

				# Add topic nodes to topics
				for topic in node.topics:
					if topic not in dupliNode.topics:
						topics[topic].sourceNodes.append(dupliNode)

				dupliNode.topics.extend(node.topics)
				dupliNode.topics = list(set(dupliNode.topics))

				# Add neighboring nodes as a new attribute
				dupliNode.neighborSources.extend([neighbor.source for neighbor in node.neighbors])
				dupliNode.neighborSources = list(set(dupliNode.neighborSources))

			# Otherwise
			else:
				# Add neighboring nodes list
				node.neighborSources = [neighbor.source for neighbor in node.neighbors]
				self.sources[source] = node

				# Add to topic nodes
				for topic in node.topics:
					topics[topic].sourceNodes.append(node)


		# Create neighbor links
		for source, node in self.sources.items():
			node.neighbors = []

			for neighbor in node.neighborSources:
				node.neighbors.append(self.sources[neighbor])
