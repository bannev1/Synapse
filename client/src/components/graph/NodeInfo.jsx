import React from 'react'
import Image from 'next/image'

// Icons
import openInNewWhite from '/public/icons/openInNewWhite.svg'


function NodeInfo({x, y, name, url, sourceName, location, medium, topics}) {
	return (
		<>
			<div className="nodeInfo" style={{'top': y, 'left': x}}>
				<p className='title'>{name}</p>

				<div>
					<p className='subtitle'>Source:</p>
					<p>{sourceName}</p>
				</div>

				<div>
					<p className='subtitle'>Location:</p>
					<p>{location}</p>
				</div>

				<div>
					<p className='subtitle'>Medium:</p>
					<p>{medium}</p>
				</div>

				<div>
					<p className='subtitle'>Topics:</p>

					<ul className='topics'>
						{
							topics.map(topic => (
								<li>{topic}</li>
							))
						}
					</ul>
				</div>

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