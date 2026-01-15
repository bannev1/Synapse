from app.models import Graph


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

		super().__init__(query, type, depth, sites)

	

	def construct(self):
		"""
		Construct compare graph
		"""

		# Get topic nodes
		