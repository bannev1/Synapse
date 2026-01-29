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

		self.graph1 = graph1
		self.graph2 = graph2

		super().__init__(query, type, depth, [])

	

	def construct(self):
		"""
		Construct compare graph
		"""

		# Get topics 
		self.topics = list(set(self.graph1['topics'] + self.graph2['topics']))

		# Go through sources and add to list
		sources = {}

		for source in (self.graph1['sources'] + self.graph2['sources']):
			# If site already exists
			if source['source'] in self.sites:
				# Add topics (no duplicates)
				sources[source['source']]['topics'] = list(set(sources[source['source']]['topics'] + source['topics']))

				# Add neighbors
				sources[source['source']]['neighbors'].extend(source['neighbors'])

			# Otherwise add source
			else:
				self.sites.append(source['source'])
				sources[source['source']] = source

		# Save locally as list
		self.sources = list(sources.values())
