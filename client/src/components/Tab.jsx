'use client';

import React, { useState } from 'react'
import Image from 'next/image'
import { redirect } from 'next/navigation';

import closeBlack from '/public/icons/closeBlack.svg'


function Tab({
	tabName,
	graph,
	onDelete,
	isCurrTab = false,
	isNewTab = false,
}) {
	if (graph == undefined && !isCurrTab)
		return null

	const [showConfirmModal, setShowConfirmModal] = useState(false)


	const closeTab = () => {
		if (!isCurrTab) {
			onDelete()
		}
	}

	const switchTab = () => {
		if (isCurrTab)
			return

		redirect(`/view/${encodeURIComponent(tabName)}`)
	}
	
	return (
		<>
			<div className={`tab ${isCurrTab ? 'active' : ''}`}>
				<div/>

				<button className='invisible' onClick={switchTab}>
					<p className={isNewTab ? 'newTab' : ''}>{isNewTab ? 'New Tab' : tabName}</p>
				</button>

				{
					!isCurrTab && // So can't close current or new tabs

					<button className='close' onClick={() => {closeTab(true)}}>
						<Image src={closeBlack} alt="Close Icon" />
					</button>
				}
			</div>
		</>
	)
}

export default Tab