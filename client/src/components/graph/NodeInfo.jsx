import React from 'react'
import Image from 'next/image'

import GraphFade from './GraphFade'

// Icons
import openInNewWhite from '/public/icons/openInNewWhite.svg'

function NodeInfo({x, y, name, url}) {
	return (
		<>
			<GraphFade>
				<div className="nodeInfo" style={{'top': y, 'left': x}}>
					<p className='title'>{name}</p>

					<button className='openLink' onClick={() => {
						window.open(url, "_blank")
					}}>
						Open Link

						<Image alt="Open Icon" src={openInNewWhite}/>
					</button>
				</div>
			</GraphFade>
		</>
	)
}

export default NodeInfo