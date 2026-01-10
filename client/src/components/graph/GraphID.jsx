import React, { useState } from 'react'
import Image from 'next/image'

// Icons
import copyBlack from '/public/icons/copyBlack.svg'
import tickBlack from '/public/icons/tickBlack.svg'


// Easy to copy+paste graph ID for save/shares
function GraphID({link}) {
	const [copiedTick, setCopiedTick] = useState(false) // To indicate copied

	return (
		<div id="graphID">
			{/* Text */}
			<input type="text" value={link} readOnly={true}/>
			
			{/* Copy text button */}
			<button onClick={() => {
				navigator.clipboard.writeText(link)
				setCopiedTick(true) // indicate then wait lik 700ms until change back

				setTimeout(() => {
					setCopiedTick(false) // turn back to normal
				}, 700)
			}}>
				<Image src={copiedTick ? tickBlack : copyBlack} alt="Copy Icon"/>
			</button>
		</div>
	)
}

export default GraphID