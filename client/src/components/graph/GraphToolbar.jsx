'use client'

import React, { useState } from 'react'
import Image from 'next/image'

// Components
import SearchComparison from './components/SearchComparison';

// Icons
import infoBlack from '/public/icons/infoBlack.svg';
import infoWhite from '/public/icons/infoWhite.svg';
import panBlack from '/public/icons/panBlack.svg';
import panWhite from '/public/icons/panWhite.svg';


function GraphToolbar({}) {
	// Tools
	const [handTool, setHandTool] = useState(0) // 0 is pan, 1 is info
	const [showComparePopup, setShowComparePopup] = useState(false)


	return (
		<div id="miniTools">
			{/* For fringes on the side */}
			<div className='sideStyle'>
				<div className='left'/>
				<div className='right'/>
			</div>

			{/* Hand buttons */}
			<div>
				<button className={handTool == 0 ? 'active' : ''} onClick={() => {setHandTool(0)}}>
					<Image src={handTool == 0 ? panBlack : panWhite} alt='Pan Icon'/>
				</button>

				<button className={handTool == 1 ? 'active' : ''} onClick={() => {setHandTool(1)}}>
					<Image src={handTool == 1 ? infoBlack : infoWhite} alt='Info Icon'/>
				</button>
			</div>

			{/* Comparison button w/ popup */}
			<div>
				<button onClick={() => setShowComparePopup(v => !v)}>

				</button>

				{
					showComparePopup &&
					<SearchComparison/>
				}
			</div>

			<div>

			</div>

			<div>

			</div>
		</div>
	)
}

export default GraphToolbar