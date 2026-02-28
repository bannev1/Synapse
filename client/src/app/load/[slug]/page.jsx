'use client'

import React, { useContext, useEffect, useState } from 'react'
import { notFound, useParams } from 'next/navigation'
import Image from 'next/image'

import '@/styles/view/styles.css'
import { loadGraph } from '@/scripts/save'

import TabBar from '@/components/TabBar'
import SearchBar from '@/components/SearchBar'
import Loading from '@/components/Loading'
import Graph from '@/components/graph/Graph'
import GraphID from '@/components/graph/GraphID'

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
		const result = loadGraph(graphID)

		// If not dictionary, means returned error code not graph
		if (!(result.constructor == Object && result != null && result !== undefined)) {
			// Console log error
			console.log(result)
			return notFound() // Show 404 page
		}

		// Save loaded graph
		setGraph(result)
		setGraphLoaded(true)
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

				<TabProvider>
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
							<GraphOptions tabName={pid} canSave={false}/>
						</div>
					</GraphProvider>
				</TabProvider>
			}
		</>
	)
}

export default Load