'use client';

import React, { useContext, useEffect, useState } from 'react'
import { notFound, useParams } from 'next/navigation';
import Image from 'next/image';

import '@/styles/view/styles.css'

// Components
import { GraphProvider } from '@/components/contexts/GraphContext';
import { TabContext, TabProvider } from '@/components/contexts/TabContext';
import Graph from '@/components/graph/Graph';
import GraphOptions from '@/components/graph/GraphOptions';
import GraphToolbar from '@/components/graph/GraphToolbar';
import TabBar from '@/components/TabBar';
import SearchBar from '@/components/SearchBar';
import SearchOptions from '@/components/SearchOptions';


function View() {
	const params = useParams()
	const pid = params.slug;

	const {tabs, setTabs} = useContext(TabContext);

	const [currTab, setTab] = useState(undefined)
	const [graph, setGraph] = useState({
		'allNodes': [],
		'allLinks': []
	})


	const [searchOptions, setSearchOptions] = useState({
		'depth': 6,
		'graphType': 'topical'
	})

	// Tools
	const [handTool, setHandTool] = useState(0) // 0 is pan, 1 is info

	const [showComparePopup, setShowComparePopup] = useState(false)

	// Find tab
	useEffect(() => {
		const foundTabs = tabs.find(tabElem => tabElem.name === pid)

		if (foundTabs) {
			const tabElem = foundTabs[0]

			setTab(tabElem)

			// Get links and nodes
			setGraph({
				'allNodes': tabElem.graph['sources'] + tabElem.graph['topics'],
				'allLinks': tabElem.graph['topicLinks'] + tabElem.graph['sourceLinks']
			})

		// Check if tab exists
		} else if (tabs.length > 0) {
			notFound()
		}
	}, [pid, tabs])

	return (
		<>
			<TabProvider>
				<TabBar isNewTab={true}/>

				<GraphProvider allNodes={graph['allNodes']} allLinks={graph['allLinks']}>
					<div id="home">
						<div id="toolbarPlaceholder"/>
						<div id="toolbar">
							<SearchBar inverted={true}/>

							<SearchOptions onChangeOptions={setSearchOptions} inverted={true}/>
						</div>

						<Graph/>
					</div>
				</GraphProvider>
			</TabProvider>
		</>
	)
}

export default View