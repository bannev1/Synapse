import React from 'react'


// Fading background of graph
function GraphFade({children = <></>}) {
	return (
		<div id="graphFade">
			<div className='fader'/>

			{children}
		</div>
	)
}

export default GraphFade