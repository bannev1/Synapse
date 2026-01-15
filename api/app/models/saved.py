from app.models.graph import Graph
from app.models.database import Database
from app.exceptions import GraphNotFound


class SavedGraph(Graph):
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
		super(Graph, self).__init__(graph['name'], graph['graphType'], -1, [])



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

		# Create base graph
		self.graph = {
			'name': self.query,
			'id': self.id,
			'topics': [],
			'sources': [],
			'topicLinks': [],
			'sourceLinks': []
		}

		# Retrieve topicNodes
		topics = {}
		for topic in self.topicNodes:
			topics[topic['id']] = topic['name']
			
		self.graph['topics'] = list(topics.values())

		# Retrieve sourceNodes
		sources = {}
		for source in self.sourceNodes:
			# Add node as dictionary
			sources[source['id']] = {
				'source': source['source'],
				'name': source['name'],
				'topics': source['topics'].split(','), # Convert CSV to list object
				'medium': source['medium'],
				'location': source['location'],
				'neighbors': []
			}

		# Make topic to source links
		for topicLink in self.topicSourceLinks:
			self.graph['topicLinks'].append({
				'target': topics[topicLink['topicNode']],
				'source': sources[topicLink['sourceNode']]['source']
			})
		
		# Make source links
		for sourceLink in self.sourceLinks:
			node1 = sources[sourceLink['sourceNode1']]
			node2 = sources[sourceLink['sourceNode2']]

			self.graph['sourceLinks'].append({
				'target': node1['source'],
				'source': node2['source']
			})

			# Add as neighbor
			node1['neighbors'].append(node2['source'])

		# Add to main graph
		self.graph['sources'] = list(sources.values())

		return self.graph


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
