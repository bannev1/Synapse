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
		self.sources: list[str] = [] # List of all sources (str URLs)

		# Construct graph
		self.construct()



	@abstractmethod
	def createTopicNodes(self) -> list[TopicNode]:
		"""
		Create the topic nodes for this class
		"""
		raise NotImplementedError("createTopicNodes() method not implemented") # Raise error if not implemented


	@abstractmethod
	def construct(self) -> Node:
		"""
		Construct a graph of this class
		"""
		raise NotImplementedError("construct() method not implemented") # Raise error if not implemented
	


	def parse(self) -> dict:
		"""
		Universal method to parse the graph into a dictionary format to send as a request
		"""
