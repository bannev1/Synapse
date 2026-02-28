"use client"

import React, { useEffect, useState, useContext } from 'react'
import { useRouter } from 'next/navigation'

import { TabContext } from '@/components/contexts/TabContext'
import { compare } from '@/scripts/search'



function SearchComparisonModal({ setShowPopup }) {
	const { tabs, setTabs } = useContext(TabContext)
	const router = useRouter()
	const [selectedTab1, setSelectedTab1] = useState('')
	const [selectedTab2, setSelectedTab2] = useState('')

	// Set default selections
	useEffect(() => {
		if (tabs.length > 0) setSelectedTab1(tabs[0].name)
		if (tabs.length > 1) setSelectedTab2(tabs[1].name)
	}, [tabs])

	const handleCompare = async () => {
		// If same tab selected
		if (!selectedTab1 || !selectedTab2 || selectedTab1 === selectedTab2) {
			alert('Please select two different tabs.')
			return
		}

		// Get tabs
		const tab1 = tabs.find(t => t.name === selectedTab1)
		const tab2 = tabs.find(t => t.name === selectedTab2)
		
		if (!tab1 || !tab2) 
			return
		
		// Fetch compare graph
		const graph1 = tab1.graph
		const graph2 = tab2.graph
		const result = await compare(graph1, graph2)

		if (result === 'error') {
			alert('Failed to compare graphs.')
			return
		}

		// Create tab
		const newGraph = result
		const newTab = { 
			name: encodeURIComponent(result.name), 
			graph: newGraph 
		}
		
		setTabs(prev => [...prev, newTab])
		setShowPopup(false)

		// Redirect
		router.push(`/view/${encodeURIComponent(result.name)}`)
	}


	return (
		<>
			<div className='modalBackdrop' onClick={() => setShowPopup(false)} />

			<div className='modal'>
				<h1>Create Compare Graph</h1>

				{/* First Graph Dropdown */}
				<label>Select first graph:</label>
				<select value={selectedTab1} onChange={e => setSelectedTab1(e.target.value)}>
					{tabs.map(tab => (
						<option key={tab.name} value={tab.name}>
							{tab.graph?.name || decodeURIComponent(tab.name)}
						</option>
					))}
				</select>

				{/* Second Graph Dropdown */}
				<label>Select second graph:</label>
				<select value={selectedTab2} onChange={e => setSelectedTab2(e.target.value)}>
					{tabs.map(tab => (
						<option key={tab.name} value={tab.name}>
							{tab.graph?.name || decodeURIComponent(tab.name)}
						</option>
					))}
				</select>

				<div className='buttons'>
					<button onClick={() => setShowPopup(false)}>Close</button>
					<button onClick={handleCompare}>Compare</button>
				</div>
			</div>
		</>
	)
}

export default SearchComparisonModal
