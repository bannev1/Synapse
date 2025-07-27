import React from 'react'

function Tab({
	tabName,
	graph,
	isCurrTab = false
}) {
  return (
	<div className="tab">
		{tabName}
	</div>
  )
}

export default Tab