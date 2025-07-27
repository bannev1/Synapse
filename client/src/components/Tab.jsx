import React from 'react'

function Tab({
	tabName,
	graph,
	isCurrTab = false
}) {
	if (graph == undefined && !isCurrTab)
		return
	
	return (
		<div className="tab">
			{tabName}
		</div>
	)
}

export default Tab