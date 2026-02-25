'use client';

import React, { useContext, useState } from 'react'
import { useRouter } from 'next/navigation';

import '@/styles/search/styles.css'

import { TabContext } from '@/components/contexts/TabContext';
import SearchBar from '@/components/SearchBar'
import TabBar from '@/components/TabBar';
import ConfirmModal from '@/components/modals/ConfirmModal';
import SearchOptions from '@/components/SearchOptions';
import { search } from '@/scripts/requests/search';
import Loading from '@/components/Loading';
import ErrorModal from '@/components/modals/ErrorModal';

function Search({forceNewTabView = false}) {
	const {tabs, setTabs} = useContext(TabContext)
	
	const tabsExist = tabs.length > 0 || forceNewTabView // If tabs, then show tab bar (or if forcing)
	const inverted = tabsExist ? '' : 'inverted'

	const [searchOptions, setSearchOptions] = useState({})

	const [loading, setLoading] = useState(false)
	const [error, setError] = useState(false)

	const router = useRouter();

	const searchQuery = async (query) => {
		if (!query || !query.trim()) {
			console.log('No query provided')
			return
		}

		// Map graphType index to string (assuming backend expects 'topical', 'medium', 'locational')
		const graphTypeMap = ['topical', 'medium', 'locational']
		const graphType = graphTypeMap[searchOptions.graphType] || 'topical'
		const depth = searchOptions.depth || 6

		// Show loading screen
		setLoading(true)

		// Perform the search
		const graph = await search(query, depth, graphType)

		if (graph === 'error') {
			console.log('Error fetching graph')
			setError(true)
			setLoading(false)
		}

		// Add a new tab
		const newTab = { 
			name: encodeURIComponent(query),
			graph: graph 
		}
		setTabs(prevTabs => [...prevTabs, newTab]);

		// Navigate to view page
		router.push(`/view/${encodeURIComponent(query)}`)
	}

	return (
		<>
			{ // Tab viewer
				tabsExist && 
				<TabBar isNewTab={true}/>
			}

			{/* Main content */}
			<div id="home" className={inverted}>
				<div style={{'position': 'relative'}}>
					<h1 className={`underline blue ${inverted}`}>Synapse</h1>
					<p id="slogan">Think connected.</p>
				</div>

				<SearchBar onSearch={searchQuery} inverted={tabsExist} placeholder="What's your next search?" height={25}/>

				<SearchOptions onChangeOptions={setSearchOptions} inverted={tabsExist}/>
			</div>
			
			{/* Search Error Modal */}
			<ErrorModal content={'Error searching for graph. See logs for more details.'} refresh={error}/>
			
			{ // Loading screen
				loading && 
				<Loading/>
			}
		</>
	)
}

export default Search