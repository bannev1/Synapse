'use client';

import React from 'react'
import Image from 'next/image'

import closeBlack from '/public/icons/closeBlack.svg'

function Tab({
	tabName,
	graph,
	isCurrTab = false
}) {
	if (graph == undefined && !isCurrTab)
		return
	
	
	return (
		<div className="tab">
			{tabName}

			<button>
				<Image src={closeBlack} alt="Close Icon" />
			</button>
		</div>
	)
}

export default Tab