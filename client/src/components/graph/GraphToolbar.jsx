'use client'

import React, { useState, useContext } from 'react'
import Image from 'next/image'

import { GraphContext } from '../contexts/GraphContext';

// Components
import SearchComparison from './components/SearchComparison';

// Icons
import infoBlack from '/public/icons/infoBlack.svg';
import infoWhite from '/public/icons/infoWhite.svg';
import panBlack from '/public/icons/panBlack.svg';
import panWhite from '/public/icons/panWhite.svg';
import compareWhite from '/public/icons/compareWhite.svg';
import compareBlack from '/public/icons/compareBlack.svg';
import fullscreenWhite from '/public/icons/fullscreenWhite.svg'


function GraphToolbar({}) {
	const {handTool, setHandTool, makeFullScreen} = useContext(GraphContext);
	const [showComparePopup, setShowComparePopup] = useState(false);


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
				<button className={showComparePopup ? 'active' : ''} onClick={() => setShowComparePopup(v => !v)}>
					<Image src={showComparePopup ? compareBlack : compareWhite} alt='Compare Icon'/>
				</button>

				{
					showComparePopup &&
					<SearchComparison/>
				}
			</div>

			{/* Full-Screen */}
			<div className='noActive'>
				<button onClick={() => makeFullScreen()}>
					<Image src={fullscreenWhite} alt='Fullscreen Icon'/>
				</button>
			</div>
		</div>
	)
}

export default GraphToolbar