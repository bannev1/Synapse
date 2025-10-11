'use client';

import React, { useContext, useState } from 'react'
import { notFound, useParams } from 'next/navigation';
import Image from 'next/image';

import '@/styles/view/styles.css'

import { TabContext, TabProvider } from '@/components/contexts/TabContext';
import TabBar from '@/components/TabBar';
import SearchBar from '@/components/SearchBar';
import SearchOptions from '@/components/SearchOptions';

// Icons
import refresh from '/public/icons/refresh.svg';
import downRed from '/public/icons/downRed.svg';
import filterRed from '/public/icons/filterRed.svg';
import compareWhite from '/public/icons/compareWhite.svg';
import zoomWhite from '/public/icons/zoomWhite.svg';
import listFilterWhite from '/public/icons/listFilterWhite.svg';
import fullscreenWhite from '/public/icons/fullscreenWhite.svg';
import fullscreenExitWhite from '/public/icons/fullscreenExitWhite.svg';
import appsWhite from '/public/icons/appsWhite.svg';

// Components
import Graph from '@/components/graph/Graph';
import { GraphProvider } from '@/components/contexts/GraphContext';


function View() {
	const params = useParams()
	const pid = params.slug;

	console.log(pid)

	const {tabs, setTabs} = useContext(TabContext);

	const [searchOptions, setSearchOptions] = useState({
		'depth': 6,
		'sources': [],
		'useAll': true
	})

	const [showListView, setShowListView] = useState(false)

	// Tools
	const [handTool, setHandTool] = useState(0) // 0 is pan, 1 is info

	const [showComparePopup, setShowComparePopup] = useState(false)

	// Find tab
	// var tab = undefined;
	// tabs.forEach(tabElem => {
	// 	if (tabElem.name == refTab)
	// 		tab = tabElem
	// });

	// Check if tab exists
	// if (tab == undefined)
	// 	notFound()

	// const graph = tab.graph;

	const listView = []

	return (
		<>
			<TabProvider>
				<TabBar isNewTab={true}/>

				<GraphProvider>
					<div id="home">
						<div id="toolbar">
							<button id="refresh">
								<Image src={refresh} alt='Refresh Icon'/>
							</button>

							<SearchBar inverted={true}/>

							<SearchOptions onChangeOptions={setSearchOptions} inverted={true}/>

							{/* <div id="listView">
								<div className={`labels ${showListView ? 'active' : ''}`} onClick={() => setShowListView(v => !v)}>
								<div>
								<Image className='downArrow' src={downRed} alt='Down Icon'/>
								<p>List View</p>
								</div>
								
								<button>
								<Image src={filterRed} alt='Filter Icon'/>
								</button>
								</div>
								
								{
									showListView &&
									<div id='listContainer'>
									{
										listView.forEach((listItem, idx) => {
											<div key={idx} className='container'></div>
											})
											}
											</div>
											}
											</div> */}
						</div>

						<Graph/>
					</div>
				</GraphProvider>
			</TabProvider>
		</>
	)
}

export default View