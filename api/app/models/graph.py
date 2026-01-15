from typing_extensions import Literal
from abc import abstractmethod

from app.models.nodes import Node, SourceNode, TopicNode


class Graph:
	def __init__(self, query: str, type: Literal['topical', 'medium', 'locational'], depth: int, sites: list[str]) -> None:
		"""
		Graph Base Class
		"""

		# Set attributes
		self.query: str = query
		self.type: Literal['topical', 'medium', 'locational'] = type
		self.depth: int = depth
		self.sites: list[str] = sites

		# Define attributes which will be set later
		self.topicNodes: list[TopicNode] = [] # List of all topicnodes (linked to sourceNodes)
		self.sources: dict[str, SourceNode] = {} # List of all sources (str URLs) and their corresponding SourceNode

		# Construct graph
		self.construct()



	@abstractmethod
	def construct(self) -> Node:
		"""
		Construct a graph of this class
		"""
		raise NotImplementedError("construct() method not implemented") # Raise error if not implemented
	

	@abstractmethod
	def findNeighboringNodes(self, node: SourceNode, currDepth: int = 1) -> list[SourceNode]:
		"""
		Find neighboring nodes given a SourceNode
		"""
		raise NotImplementedError("findNeighboringNodes() method not implemented") # Raise error if not implemented



	def parse(self) -> dict:
		"""
		Universal method to parse the graph into a dictionary format to send as a request
		"""

		# Create base graph
		self.graph = {
			'name': self.query,
			'type': self.type,
			'depth': self.depth,
			'sources': self.sources.keys(),
			'topics': [topic.name for topic in self.topicNodes], # Get each topic by name as string
			'sources': [],
			'topicLinks': [],
			'sourceLinks': []
		}

		# Go through each topic node and recursively get sources + sourceNode Links
		traversed = [] # list of sources traversed (str to keep less memory)

		for topic in self.topicNodes:
			for source in topic.sourceNodes:
				self.parseSourceNodes(source, traversed)



	def parseSourceNodes(self, node: SourceNode, traversed: list[str]) -> None:
		"""
		Parse source nodes recursively to get links and sources
		"""

		traversed.append(node.source)
