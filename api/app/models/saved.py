from app.models.requestGraph import RequestGraph
from app.models.database import Database
from app.exceptions import GraphNotFound


class SavedGraph(RequestGraph):
	def __init__(self, id: str) -> None:
		'''
		Model for saved graph
		'''

		# Set own attribute
		self.id = id

		# Find graph by ID
		graph = Database().fetch(f'SELECT name, graphType FROM saved WHERE id=\'{id}\';')

		# Check if any
		if len(graph) != 1:
			raise GraphNotFound(f'No saved graph at {id=}')
		
		graph = graph[0]
		
		# Save attributes of inherited function
		super().__init__(None)
		
		self.query = graph[0]
		self.type = graph[1]



	def construct(self) -> None: 
		'''
		Convert saved graph links
		'''
		
		# Retrieve topic nodes and source nodes
		self.topicNodes = Database().fetch(f'SELECT id, name FROM savedTopicNodes WHERE graph=\'{self.id}\';')
		self.sourceNodes = Database().fetch(f'SELECT id, name, source, sourceName, location, medium, topics FROM savedSourceNodes WHERE graph=\'{self.id}\';')
		
		# Retrieve links
		self.topicSourceLinks = Database().fetch(f'SELECT topicNode, sourceNode FROM savedTopicSourceJoinTable WHERE graph=\'{self.id}\';')
		self.sourceLinks = Database().fetch(f'SELECT sourceNode1, sourceNode2 FROM savedSourceSourceJoinTable WHERE graph=\'{self.id}\';')



	def parse(self) -> dict:
		'''
		Convert saved retrieved graph into dictionary format
		'''

		# Add base attributes
		self.graph = {
			'name': self.query,
			'depth': self.depth,
			'type': self.type
		}

		# Retrieve topicNodes
		topics = {}
		for topic in self.topicNodes:
			topics[topic[0]] = topic[1]
			
		self.graph['topics'] = list(topics.values())

		# Retrieve sourceNodes
		sources = {}
		for source in self.sourceNodes:
			# Add node as dictionary
			sources[source[0]] = {
				'id': source[2],
				'source': source[2],
				'name': source[1],
				'sourceName': source[3],
				'location': source[4],
				'medium': source[5],
				'topics': source[6].split(','), # Convert CSV to list object
				'neighbors': []
			}

		# Clear graph
		self.graph['topicLinks'] = []
		self.graph['sourceLinks'] = []

		# Make topic to source links
		for topicLink in self.topicSourceLinks:
			self.graph['topicLinks'].append({
				'target': topics[topicLink[0]],
				'source': sources[topicLink[1]]['source']
			})
		
		# Make source links
		for sourceLink in self.sourceLinks:
			node1 = sources[sourceLink[0]]
			node2 = sources[sourceLink[1]]

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
	def updateByID(id: str, graph: RequestGraph) -> None:
		'''
		Update graph in database after changes made (given the parsed graph)
		'''

		# Delete original graph
		SavedGraph.deleteByID(id)

		# Save graph at ID
		SavedGraph.saveGraph(graph, graphID=id)


	@staticmethod
	def saveGraph(graph: RequestGraph,  graphID: str = None) -> str:
		'''
		Save graph to the Saved database and return its ID
		'''

		# Parse graph
		parsed = graph.parse()

		# Save base graph
		if graphID == None: # Check if given ID otherwise let SQL generate
			graphID = Database().modifyAndReturn(f'''
				INSERT INTO saved (name, graphType) 
				VALUES ('{graph.query.replace("'", "''")}', '{graph.type}') 
				RETURNING id;''')[0]
		else:
			Database().modify(f'''
				INSERT INTO saved (id, name, graphType) 
				VALUES ('{graphID}', '{graph.query.replace("'", "''")}', '{graph.type}';''')

		# Save all sourceNodes
		sourceNodes = {} # Dict of (source, id)

		for node in parsed['sources']:
			nodeTopics = ','.join(node['topics']) 
			nodeID = Database().modifyAndReturn(f'''
				INSERT INTO savedSourceNodes (graph, name, source, sourceName, location, medium, topics)
				VALUES ('{graphID}', '{node['name'].replace("'", "''")}', '{node['source'].replace("'", "''")}', '{node['sourceName'].replace("'", "''")}', '{node['location'].replace("'", "''")}', '{node['medium'].replace("'", "''")}', '{nodeTopics.replace("'", "''")}')
				RETURNING id;''')[0]
			
			sourceNodes[node['source']] = nodeID
		
		
		# Save all topic nodes
		topicNodes = {} # Dict of (topic, id)
		
		for topic in parsed['topics']:
			topicID = Database().modifyAndReturn(f'''
				INSERT INTO savedTopicNodes (graph, name)
				VALUES ('{graphID}', '{topic.replace("'", "''")}')
				RETURNING id;''')[0]
			
			topicNodes[topic] = topicID

		# Save topic-source links
		for link in parsed['topicLinks']:
			topicID = topicNodes[link['target']]
			sourceID = sourceNodes[link['source']]

			Database().modify(f'''
							INSERT INTO savedTopicSourceJoinTable (graph, topicNode, sourceNode)
					 		VALUES ('{graphID}', '{topicID}', '{sourceID}');''')

		# Save source-source links
		for link in parsed['sourceLinks']:
			node1 = sourceNodes[link['target']]
			node2 = sourceNodes[link['source']]

			Database().modify(f'''
							INSERT INTO savedSourceSourceJoinTable (graph, sourceNode1, sourceNode2)
					 		VALUES ('{graphID}', '{node1}', '{node2}');''')
			
		# Return ID
		return graphID

	
	@staticmethod
	def deleteByID(id: str) -> None:
		'''
		Delete a SavedGraph given its ID
		'''

		Database().modify(f'DELETE FROM saved WHERE id=\'{id}\';')
