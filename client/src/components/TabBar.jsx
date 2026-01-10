'use client'

import React, { useContext, useEffect } from 'react'
import { TabContext } from './contexts/TabContext'
import Tab from './Tab'

import addWhite from '/public/icons/addWhite.svg'
import Image from 'next/image'
import { redirect } from 'next/navigation'


function TabBar({ currTab = '', isNewTab = false }) {
	const {tabs} = useContext(TabContext)
	
	return (
		<div id="tabGroup">
			{/* Logo */}
			<h1 id="tabLogo" className='underline blue inverted'>
				Synapse
			</h1>

			<div id="tabs">
				{ // New 'tab' (false tab)
					isNewTab && 
					<Tab isNewTab={true} isCurrTab={true} graph={undefined}/>
				}

				{ // Get all tabs
					tabs.forEach(tab => {
						<Tab tabName={tab.name} isCurrTab={isNewTab || currTab==tab.name} graph={tab.graph}/>
					})
				}

				{/* Add tab button (when not already new tab) */}
				{
					!isNewTab &&
					<button id="addTab" onClick={() => {redirect('/view')}}>
						<Image src={addWhite} alt='Add Icon'/>
					</button>
				}
			</div>
		</div>
	)
}

export default TabBar