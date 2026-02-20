'use client';

import React, { useContext, useState } from 'react'

import SearchBar from '@/components/SearchBar'
import TabBar from '@/components/TabBar';
import '@/styles/search/styles.css'
import { TabContext } from '@/components/contexts/TabContext';
import ConfirmModal from '@/components/modals/ConfirmModal';
import SearchOptions from '@/components/SearchOptions';

function Search({forceNewTabView = false}) {
	const {tabs, setTabs} = useContext(TabContext)
	
	const tabsExist = tabs.length > 0 || forceNewTabView // If tabs, then show tab bar (or if forcing)
	const inverted = tabsExist ? '' : 'inverted'

	const [searchOptions, setSearchOptions] = useState({})

	const searchQuery = () => {
		// Add 
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
		</>
	)
}

export default Search