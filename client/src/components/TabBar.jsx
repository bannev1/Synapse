import React, { useContext } from 'react'
import { TabContext } from './contexts/TabContext'
import Tab from './Tab'

import addWhite from '/public/icons/addWhite.svg'
import Image from 'next/image'
import { redirect } from 'next/navigation'


function TabBar({ currTab, isNewTab = false }) {
	const {tabs, setTabs} = useContext(TabContext)

	if (!isNewTab && currTab != '')
		return
	
	
	return (
		<div id="tabGroup">
			<h1 id="tabLogo" className='underline blue inverted'>
				Synapse
			</h1>

			<div id="tabs">
				{
					isNewTab && 
					<Tab tabName='New Tab' isCurrTab={true} graph={undefined}/>
				}

				{
					tabs.forEach(tab => {
						<div className="tab"></div>
					})
				}

				<button id="addTab" onClick={() => {redirect('/search')}}>
					<Image src={addWhite} alt='Add Icon'/>
				</button>
			</div>
		</div>
	)
}

export default TabBar