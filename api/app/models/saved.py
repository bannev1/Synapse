from app.models.graph import Graph
from app.models.requestGraph import RequestGraph
from app.models.database import Database
from app.exceptions import GraphNotFound


class SavedGraph(RequestGraph):
	def __init__(self, id: str) -> None:
		"""
		Model for saved graph
		"""

		# Set own attribute
		self.id = id

		# Find graph by ID
		graph = Database().fetch(f"SELECT name, graphType FROM saved WHERE id={id};")

		# Check if any
		if len(graph) != 1:
			raise GraphNotFound(f"No saved graph at {id=}")
		
		graph = graph[0]
		
		# Save attributes of inherited function
		super(RequestGraph, self).__init__({
			'name': graph['name'],
			'id': id,
			'type': graph['graphType'], 
			'depth': -1,
			'sources': []
		})



	def construct(self) -> None: 
		"""
		Convert saved graph links
		"""
		
		# Retrieve topic nodes and source nodes
		self.topicNodes = Database().fetch(f'SELECT id, name FROM savedTopicNodes WHERE graph={self.id};')
		self.sourceNodes = Database().fetch(f'SELECT id, name, source, location, medium, topics FROM savedSourceNodes WHERE graph={self.id};')
		
		# Retrieve links
		self.topicSourceLinks = Database().fetch(f'SELECT topicNode, sourceNode FROM savedTopicSourceJoinTable WHERE graph={self.id};')
		self.sourceLinks = Database().fetch(f'SELECT sourceNode1, sourceNode2 FROM savedSourceSourceJoinTable WHERE graph={self.id};')



	def parse(self) -> dict:
		"""
		Convert saved retrieved graph into dictionary format
		"""

		return super(RequestGraph, self).parse()


	@staticmethod
	def updateByID(id: str, graph: Graph) -> None:
		"""
		Update graph in database after changes made (given the parsed graph)
		"""

		# Delete original graph
		SavedGraph.deleteByID(id)

		# Save graph at ID
		SavedGraph.saveGraph(graph, graphID=id)


	@staticmethod
	def saveGraph(graph: Graph,  graphID: str = None) -> str:
		"""
		Save graph to the Saved database and return its ID
		"""

		# Parse graph
		parsed = graph.parse()

		# Save base graph
		sources = ','.join(sorted(graph.sources)) # Convert to CSV

		# Check if given ID otherwise let SQL generate
		if graphID == None:
			graphID = Database().modifyAndReturn(f"""
				INSERT INTO saved (query, graphType, depth, sources) 
				VALUES ({graph.query}, {graph.type}, {graph.depth}, {sources}) 
				RETURNING id;""")['id']
		else:
			Database().modify(f"""
				INSERT INTO saved (query, graphType, depth, sources) 
				VALUES ({graph.query}, {graph.type}, {graph.depth}, {sources})""")

		# Save all sourceNodes
		sourceNodes = {} # Dict of (source, id)

		for node in parsed['sources']:
			nodeTopics = ','.join(node['topics']) 
			nodeID = Database().modifyAndReturn(f"""
				INSERT INTO savedSourceNodes (graph, name, source, location, medium, topics)
				VALUES ({graphID}, {node['name']}, {node['source']}, {node['location']}, {node['medium']}, {nodeTopics})
				RETURNING id;""")['id']
			
			sourceNodes[node['source']] = nodeID
		
		
		# Save all topic nodes
		topicNodes = {} # Dict of (topic, id)
		
		for topic in parsed['topics']:
			topicID = Database().modifyAndReturn(f"""
				INSERT INTO savedTopicNodes (graph, name)
				VALUES ({graphID}, {topic})
				RETURNING id;""")['id']
			
			topicNodes[topic] = topicID

		# Save topic-source links
		for link in parsed['topicLinks']:
			topicID = topicNodes[link['target']]
			sourceID = sourceNodes[link['source']]

			Database().modify(f"""
							INSERT INTO savedTopicSourceJoinTable (graph, topicNode, sourceNode)
					 		VALUES ({graphID}, {topicID}, {sourceID});""")

		# Save source-source links
		for link in parsed['sourceLinks']:
			node1 = sourceNodes[link['target']]
			node2 = sourceNodes[link['source']]

			Database().modify(f"""
							INSERT INTO savedSourceSourceJoinTable (graph, sourceNode1, sourceNode2)
					 		VALUES ({graphID}, {node1}, {node2});""")
			
		# Return ID
		return graphID

	
	@staticmethod
	def deleteByID(id: str) -> None:
		"""
		Delete a SavedGraph given its ID
		"""

		Database().modify(f"DELETE FROM saved WHERE id={id};")
