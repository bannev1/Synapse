import React from 'react'
import Image from 'next/image'

// Icons
import openInNewWhite from '/public/icons/openInNewWhite.svg'


function NodeInfo({x, y, name, url}) {
	return (
		<>
			<div className="nodeInfo" style={{'top': y, 'left': x}}>
				<p className='title'>{name}</p>

				<button className='openLink' onClick={() => {
					window.open(url, "_blank")
				}}>
					Open Link

					<Image alt="Open Icon" src={openInNewWhite}/>
				</button>
			</div>
		</>
	)
}

export default NodeInfo