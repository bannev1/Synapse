import React, { useState } from 'react'
import Image from 'next/image'

// Icons
import copyWhite from '@/icons/copyWhite.svg'
import tickWhite from '@/icons/tickWhite.svg'


// Easy to copy+paste graph ID for save/shares
function GraphID({id}) {
	const [copiedTick, setCopiedTick] = useState(false) // To indicate copied

	return (
		<div id="graphID">
			{/* Text */}
			<input type="text" value={id} readOnly={true}/>
			
			{/* Copy text button */}
			<button onClick={() => {

			}}>
				<Image src={copiedTick ? tickWhite : copyWhite} alt="Copy Icon"/>
			</button>
		</div>
	)
}

export default GraphID