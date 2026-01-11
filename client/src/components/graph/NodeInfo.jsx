import React from 'react'

import GraphFade from './GraphFade'

function NodeInfo({x, y, name, url}) {
	return (
		<>
			<GraphFade>
				<div className="nodeInfo">
					<p className='title'>{name}</p>
				</div>
			</GraphFade>
		</>
	)
}

export default NodeInfo