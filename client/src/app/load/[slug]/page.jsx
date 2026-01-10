'use client'

import React, { useContext, useEffect, useState } from 'react'
import { notFound, useParams } from 'next/navigation'

import '@/styles/view/styles.css'

import TabBar from '@/components/TabBar'
import SearchBar from '@/components/SearchBar'
import Loading from '@/components/Loading'
import { TabContext, TabProvider } from '@/components/contexts/TabContext'
import { loadID } from '@/scripts/requests/load'


function LoadGraph() {
	const params = useParams()
	const graphID = params.slug

	const [graphLoaded, setGraphLoaded] = useState(false) // If graph loaded
	const [graph, setGraph] = useState({})

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
		setGraph(loadGraph)
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
			<TabProvider>
				{/* Tab bar */}
				<TabBar/>

				{/* Main Page */}
				<div id="home">
					<div id="toolbar">
						<SearchBar editable={false} inverted={true} isPlaceholder={false}/>
					</div>

				</div>

				{/*  */}
			</TabProvider>
		</>
	)
}

export default LoadGraph