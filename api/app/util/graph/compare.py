from app.models import RequestGraph


class CompareGraph(RequestGraph):
	def __init__(self, graph1: dict, graph2: dict) -> None:
		"""
		Graph to compare two graphs (graphs given in JSON/dict format)
		"""

		# Set basic attributes
		query = f'{graph1["name"]} + {graph2["name"]}'
		graphType = f'{graph1["type"]} + {graph2["type"]}' if graph1["type"] != graph2["type"] else graph1["type"] # Either add types or change
		depth = max(graph1["depth"], graph2["depth"]) # Max depth of both graphs

		self.graph1 = graph1
		self.graph2 = graph2
		self.sites = [] # List of all sites

		super().__init__(None)
		self.query = query
		self.type = graphType
		self.depth = depth

	

	def construct(self):
		"""
		Construct compare graph
		"""

		# Get topics 
		self.topics = list(set(self.graph1['topics'] + self.graph2['topics'])) # Remove duplicates
		
		# Add topic links
		self.sourceLinks = (self.graph1['sourceLinks'] + self.graph2['sourceLinks'])
		self.topicLinks = (self.graph1['topicLinks'] + self.graph2['topicLinks'])

		# Go through sources and add to list
		sources = {}

		for source in (self.graph1['sources'] + self.graph2['sources']):
			url = source['source']

			# If site already exists
			if url in self.sites:
				# Add topics (no duplicates)
				sources[url]['topics'] = list(set(sources[url]['topics'] + source['topics']))

				# Add neighbors (no duplicates)
				sources[url]['neighbors'] = list(set(sources[url]['neighbors'] + source['neighbors']))

			# Otherwise add source
			else:
				self.sites.append(url)
				sources[url] = source

		# Save locally
		self.sourceNodes = list(sources.values())
