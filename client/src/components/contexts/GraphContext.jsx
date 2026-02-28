'use client';

import React, { createContext, useState, useEffect } from 'react'

import { assignColorTopics, colorNodes } from '@/scripts/color';


export const GraphContext = createContext();

export const GraphProvider = ({ allNodes, allLinks, graph, children }) => {
	const [rawGraph, setRawGraph] = useState(graph || {});
	const [handTool, setHandTool] = useState(0);
	const [nodes, setNodes] = useState(allNodes || []);
	const [links, setLinks] = useState(allLinks || []);
	const [highlightNodes, setHighlightNodes] = useState([]);
	const [selectedNode, setSelectedNode] = useState(null);
	
	useEffect(() => {
		setNodes(allNodes || [])
	}, [allNodes])

	useEffect(() => {
		setLinks(allLinks || [])
	}, [allLinks])

	useEffect(() => {
		setRawGraph(graph || [])
	}, [graph])


	const updateProvidedGraph = (newGraph) => {
		// Get sourceNodes
		const sources = newGraph.sources || []
		const sourceNodes = sources.map(source => ({
			...source,
			group: 'source' // Add group
		}))

		// Get topicNodes
		const topics = newGraph.topics || []
		const topicNodes = topics.map(topic => ({
			id: topic,
			name: topic,
			group: 'topic'
		}))

		// Create Title Node
		const title = newGraph.name || decodeURIComponent(pid)
		const titleNode = {
			id: 'titleNode',
			name: title,
			group: 'title'
		}

		// Link TitleNode to topicNodes
		const titleLinks = topics.map(topic => ({
			target: topic,
			source: 'titleNode'
		}))

		// Color nodes
		const topicColors = assignColorTopics(topics)
		const coloredNodes = colorNodes(topicColors, [
			...sourceNodes,
			...topicNodes,
			titleNode
		])

		// Set graph
		setNodes(coloredNodes)

		setLinks([
			// Deepcopy objects
			...(newGraph.topicLinks || []).map(link => ({ ...link })),
			...(newGraph.sourceLinks || []).map(link => ({ ...link })),
			...titleLinks
		])

		// Update raw graph
		setRawGraph(newGraph)
	}


	return (
		<GraphContext.Provider value={{
			rawGraph, setRawGraph,
			handTool, setHandTool, 
			nodes, setNodes, 
			links, setLinks,
			highlightNodes, setHighlightNodes,
			selectedNode, setSelectedNode,
			updateProvidedGraph
		}}>
			{children}
		</GraphContext.Provider>
	)
}
