'use client'

import React, { useContext, useEffect, useState } from 'react'
import { notFound, useParams } from 'next/navigation'
import Image from 'next/image'

import '@/styles/view/styles.css'
import { loadGraph, updateGraph } from '@/scripts/save'
import { assignColorTopics, colorNodes } from '@/scripts/color'

import TabBar from '@/components/TabBar'
import SearchBar from '@/components/SearchBar'
import Loading from '@/components/Loading'
import Graph from '@/components/graph/Graph'
import GraphID from '@/components/graph/GraphID'
import GraphOptions from '@/components/graph/GraphOptions'

import { GraphContext, GraphProvider } from '@/components/contexts/GraphContext'

// Icons
import saveWhite from '/public/icons/saveWhite.svg'


function Load() {
	const params = useParams()
	const graphID = params.slug
	const url = window.location.href
	
	const [graph, setGraph] = useState({})
	const [rawGraph, setRawGraph] = useState({})
	const [graphLoaded, setGraphLoaded] = useState(false) // If graph loaded

	// Log
	console.log(graphID)

	// Load graph
	useEffect(() => {
		const fetchGraph = async () => {
			const result = await loadGraph(graphID)

			// Check for error response
			if (result === 'error') {
				console.log(result)
				return notFound() // Show 404 page
			}

			// Get sourceNodes
			const sources = result.sources || []
			const sourceNodes = sources.map(source => ({
				...source,
				group: 'source' // Add group
			}))

			// Get topicNodes
			const topics = result.topics || []
			const topicNodes = topics.map(topic => ({
				id: topic,
				name: topic,
				group: 'topic'
			}))

			// Create Title Node
			const title = result.name || decodeURIComponent(pid)
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

			// Get type of graph
			const graphType = result.type || 'topical'
			const types = ['topical', 'medium', 'locational']

			// Set graph
			setGraph({
				allNodes: coloredNodes,

				allLinks: [
					// Deepcopy objects
					...(result.topicLinks || []).map(link => ({ ...link })),
					...(result.sourceLinks || []).map(link => ({ ...link })),
					...titleLinks
				],

				depth: result.depth || 0,
				type: types.indexOf(graphType)
			});

			console.log(graph)
			
			setRawGraph(result)
			setGraphLoaded(true)
		}

		fetchGraph()
	}, [])
	
	return (
		<>
			{/* Loading for graph */}
			{
				graphLoaded ?

				<GraphProvider allNodes={graph.allNodes} allLinks={graph.allLinks} graph={rawGraph}>
					<Loaded graphID={graphID} url={url}/>
				</GraphProvider> :

				<Loading/>
			}
		</>
	)
}


function Loaded({
	graphID,
	url
}) {
	const { rawGraph } = useContext(GraphContext)

	const saveUpdatedGraph = async () => {
		const result = updateGraph(graphID, rawGraph)

		if (result === 'error')
			console.log('Error saving')
	}

	return (
		<>
			{/* Tab bar */}
			<TabBar/>

			{/* Main Page */}
			<div id="home">
				{/* Graph Toolbar */}
				<div id="toolbarPlaceholder"/>
				<div id="toolbar">
					<SearchBar editable={false} inverted={true} isPlaceholder={false} placeholder={graph.name}/>
				
					{/* URL for copy paste */}
					<GraphID link={url}/>

					{/* Save Icon */}
					<button id="save" onClick={saveUpdatedGraph}>
						<Image src={saveWhite} alt='Save Icon'/>
					</button>
				</div>
			
				{/* Graph */}
				<Graph/>

				{/* Graph Toolbar/Options */}
				<GraphOptions tabName={''} canSave={false}/>
			</div>
		</>
	)
}


export default Load