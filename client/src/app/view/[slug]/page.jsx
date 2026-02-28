'use client';

import React, { useContext, useEffect, useState } from 'react'
import { notFound, useParams } from 'next/navigation';

import '@/styles/view/styles.css'

// Components
import { GraphProvider } from '@/components/contexts/GraphContext';
import { TabContext } from '@/components/contexts/TabContext';
import Graph from '@/components/graph/Graph';
import TabBar from '@/components/TabBar';
import SearchBar from '@/components/SearchBar';
import SearchOptions from '@/components/SearchOptions';
import Loading from '@/components/Loading';

import { assignColorTopics, colorNodes } from '@/scripts/color';
import GraphOptions from '@/components/graph/GraphOptions';


export default function View() {
	const params = useParams()
	const pid = params.slug

	const { tabs } = useContext(TabContext)

	const [currTab, setTab] = useState(undefined)
	const [graph, setGraph] = useState({
		allNodes: [],
		allLinks: [],
		depth: 0,
		type: 0
	})


	// Find the current tab + load its graph
	useEffect(() => {
		const matchingTab = tabs.find(tabElem => tabElem.name === pid)

		console.log(tabs)

		// If found tab
		if (matchingTab) {
			setTab(matchingTab)

			// Get sourceNodes
			const sources = matchingTab.graph?.sources || []
			const sourceNodes = sources.map(source => ({
				...source,
				group: 'source' // Add group
			}))

			// Get topicNodes
			const topics = matchingTab.graph?.topics || []
			const topicNodes = topics.map(topic => ({
				id: topic,
				name: topic,
				group: 'topic'
			}))

			// Create Title Node
			const title = matchingTab.graph?.name || decodeURIComponent(pid)
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
			const graphType = matchingTab.graph?.type || 'topical'
			const types = ['topical', 'medium', 'locational']

			// Set graph
			setGraph({
				allNodes: coloredNodes,

				allLinks: [
					// Deepcopy objects
					...(matchingTab.graph?.topicLinks || []).map(link => ({ ...link })),
					...(matchingTab.graph?.sourceLinks || []).map(link => ({ ...link })),
					...titleLinks
				],

				depth: matchingTab.graph?.depth || 0,
				type: types.indexOf(graphType)
			});

			console.log(graph)
		} else if (tabs.length > 0) {
			// Only 404 if tabs loaded and tab doesn't exist
			notFound()
		}
	}, [pid, tabs])


	// Simple loading state while tabs are empty
	if (tabs.length === 0)
		return <Loading/>


	// If valid tab, render everything
	return (
		<GraphProvider allNodes={graph.allNodes} allLinks={graph.allLinks} >
			<TabBar 
				currTab={currTab ? currTab.name : ''} 
			/>

			<div id="home">
				<div id="toolbarPlaceholder" />

				<div id="toolbar">
					<SearchBar inverted={true} editable={false} placeholder={currTab?.graph?.name || decodeURIComponent(pid)} isPlaceholder={false} />
					<SearchOptions onChangeOptions={() => {}} inverted={true} canEdit={false} defaultDepth={graph.depth} defaultType={graph.type} />
				</div>

				<Graph/>

				<GraphOptions tabName={pid} graph={graph}/>
			</div>
		</GraphProvider>
	)
}
