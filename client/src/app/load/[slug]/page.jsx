'use client'

import React, { useEffect, useState } from 'react'
import { notFound, useParams } from 'next/navigation'
import Image from 'next/image'

import '@/styles/view/styles.css'
import { loadGraph } from '@/scripts/save'
import { assignColorTopics, colorNodes } from '@/scripts/color'

import TabBar from '@/components/TabBar'
import SearchBar from '@/components/SearchBar'
import Loading from '@/components/Loading'
import Graph from '@/components/graph/Graph'
import GraphID from '@/components/graph/GraphID'
import GraphOptions from '@/components/graph/GraphOptions'

import { GraphProvider } from '@/components/contexts/GraphContext'

// Icons
import saveWhite from '/public/icons/saveWhite.svg'


function Load() {
	const params = useParams()
	const graphID = params.slug
	const url = window.location.href

	const [graphLoaded, setGraphLoaded] = useState(false) // If graph loaded
	const [graph, setGraph] = useState({})

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
			
			setGraphLoaded(true)
		}

		fetchGraph()
	}, [])

	return (
		<>
			{/* Loading for graph */}
			{
				!graphLoaded &&
				<Loading/>
			}


			{/* Main page */}
			{
				graphLoaded &&
				<>
					{/* Tab bar */}
					<TabBar/>


					{/* Main Page */}
					<GraphProvider
						allNodes={graph.allNodes}
						allLinks={graph.allLinks}
						graph={graph}
					>
						<div id="home">
							{/* Graph Toolbar */}
							<div id="toolbarPlaceholder"/>
							<div id="toolbar">
								<SearchBar editable={false} inverted={true} isPlaceholder={false} placeholder={graph.name}/>
							
								{/* URL for copy paste */}
								<GraphID link={url}/>

								{/* Save Icon */}
								<button id="save">
									<Image src={saveWhite} alt='Save Icon'/>
								</button>
							</div>
						
							{/* Graph */}
							<Graph/>

							{/* Graph Toolbar/Options */}
							<GraphOptions tabName={''} canSave={false}/>
						</div>
					</GraphProvider>
				</>
			}
		</>
	)
}

export default Load