import React, { useContext } from 'react'
import { TabContext } from './TabContext'
import Tab from './Tab'


function TabBar({ currTab, isNewTab = false }) {
	const {tabs, setTabs} = useContext(TabContext)

	if (isNewTab && currTab != '')
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
			</div>
		</div>
	)
}

export default TabBar