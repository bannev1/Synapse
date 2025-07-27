import React, { useContext } from 'react'
import { TabContext } from './TabContext'
import Tab from './Tab'


function TabBar({ currTabIndex, isNewTab = false }) {
	const {tabs, setTabs} = useContext(TabContext)

	if (isNewTab && currTabIndex < 0)
		return

	if (currTabIndex > tabs.length - 1)
		return
	
	
	return (
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
	)
}

export default TabBar