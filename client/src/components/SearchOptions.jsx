'use client'

import React, { useEffect, useState } from 'react'
import Image from 'next/image';

import addBlack from '/public/icons/addBlack.svg';
import removeBlack from '/public/icons/removeBlack.svg';
import addWhite from '/public/icons/addWhite.svg';
import removeWhite from '/public/icons/removeWhite.svg';
import dropdownWhite from '/public/icons/dropdownWhite.svg';
import dropdownBlack from '/public/icons/dropdownBlack.svg';


function SearchOptions({
	onChangeOptions,
	inverted = false,
	canEdit = true
}) {
	const [depthVal, setDepthVal] = useState(6)
	const [showGraphTypes, setShowGraphTypes] = useState(false)
	const [graphType, setGraphType] = useState(0) // either 0 for topical, 1 for medium, and 2 for location
	
	const graphTypes =[
		'Topical',
		'Medium',
		'Locational'
	]

	useEffect(() => {
		onChangeOptions({
			'depth': depthVal,
			'graphType': graphType
		})

	}, [depthVal, graphType])

	return (
		<div id="searchOptions" className={(inverted ? 'inverted ' : '') + (!canEdit ? 'noEdit' : '')}>
			{/* Depth Selector */}
			<div id='depthSelect'>
				{ // Plus button
					canEdit &&

					<button onClick={() => {
							if (canEdit)
								setDepthVal(v => Math.min(9, v + 1))
						}}>

						<Image src={inverted ? addBlack : addWhite} alt='Add Icon' />
					</button>
				}

				<label htmlFor='depthSelector'>Depth</label>
				<input type='text' name='depthSelector' value={depthVal} readOnly/>

				{ // Minus button
					canEdit &&

					<button onClick={() => {
							if (canEdit)
								setDepthVal(v => Math.max(1, v - 1))
						}}>

						<Image src={inverted ? removeBlack : removeWhite} alt='Remove Icon'/>
					</button>
				}
			</div>

			{/* Graph Type Selector */}
			<div id='graphType'>
				{ // Graph type
					canEdit ?

					<button className={showGraphTypes ? 'active' : ''} onClick={() => {
							if (canEdit)
								setShowGraphTypes(v => !v)
						}}>

						<p>{graphTypes[graphType]}</p>

						<Image src={inverted ? dropdownBlack : dropdownWhite} alt="Dropdown Icon" className={showGraphTypes ? 'rotate' : ''}/>
					</button> : 

					<p>{graphTypes[graphType]}</p>
				}

				{/* Graph Type Dropdown */}
				{ showGraphTypes &&
					<div className='dropdown'>
						{
							graphTypes.map((val, index) => {
								return <div key={index} className={`type ${graphType == index ? 'active' : ''}`} onClick={() => {
											if (canEdit) {
												setGraphType(index)
												setShowGraphTypes(false)
											}
										}}>

										{val}
									</div>
							})
						}
					</div>
				}
			</div>

		</div>
  )
}

export default SearchOptions