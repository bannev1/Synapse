import React from 'react'


// Fading background of graph
function GraphFade({children = <></>}) {
	return (
		<div id="graphFade">
			{children}
		</div>
	)
}

export default GraphFade