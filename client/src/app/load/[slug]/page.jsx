'use client'

import React, { useContext, useEffect, useState } from 'react'
import { notFound, useParams } from 'next/navigation'

import '@/styles/view/styles.css'
import { loadID } from '@/scripts/requests/load'

import TabBar from '@/components/TabBar'
import SearchBar from '@/components/SearchBar'
import Loading from '@/components/Loading'
import Graph from '@/components/graph/Graph'

import { TabContext, TabProvider } from '@/components/contexts/TabContext'
import { GraphProvider } from '@/components/contexts/GraphContext'

// Icons
import saveWhite from '@icons/saveWhite.svg'


function LoadGraph() {
	const params = useParams()
	const graphID = params.slug

	const [graphLoaded, setGraphLoaded] = useState(false) // If graph loaded
	const [graph, setGraph] = useState({
		"name": "My Graph",
		"allNodes": [{
					'id': 'id1',
					'site': 'NY Times',
					'url': 'https://nytimes.com',
					'group': 'source'
				},{'id': 'id2',
					'site': 'BBC',
					'url': 'https://bbc.com',
					'group': 'source'
				}],
		"allLinks": [{
					'target': 'id1',
					'source': 'id2',
				}]
	})

	// Log
	console.log(graphID)

	// Load graph
	useEffect(() => {
		const loadGraph = loadID(graphID)

		// If not dictionary, means returned error code not graph
		if (!(loadGraph.constructor == Object && loadGraph != null && loadGraph !== undefined)) {
			// Console log error
			console.log(loadGraph)
			return notFound() // Show 404 page
		}

		// Save loaded graph
		// setGraph(loadGraph)
		setGraphLoaded(true)
	}, [])

	// Load tabs context
	const {tabs, setTabs} = useContext(TabContext);

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

				<TabProvider>
					{/* Tab bar */}
					<TabBar/>


					{/* Main Page */}
					<GraphProvider
						allNodes={graph.allNodes}
						allLinks={graph.allLinks}
					>
						<div id="home">
							{/* Graph Toolbar */}
							<div id="toolbar">
								<SearchBar editable={false} inverted={true} isPlaceholder={false} placeholder={graph.name}/>
							
								{/* URL for copy paste */}
							</div>
						
							{/* Graph */}
							<Graph/>
						</div>
					</GraphProvider>
				</TabProvider>
			}
		</>
	)
}

export default LoadGraph