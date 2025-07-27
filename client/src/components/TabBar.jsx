import React, { useContext } from 'react'
import { TabContext } from './TabContext'


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
				<div className="tab"></div>
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