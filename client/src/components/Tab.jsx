'use client';

import React, { useState } from 'react'
import Image from 'next/image'
import { redirect } from 'next/navigation';

import closeBlack from '/public/icons/closeBlack.svg'
import ConfirmModal from './modals/ConfirmModal';

function Tab({
	tabName,
	graph,
	isCurrTab = false
}) {
	if (graph == undefined && !isCurrTab)
		return

	const [showConfirmModal, setShowConfirmModal] = useState(false)


	const closeTab = () => {

	}

	const switchTab = () => {
		if (isCurrTab)
			return

		redirect(`/view/${tabName}`)
	}
	
	return (
		<>
			{
				showConfirmModal &&
				<ConfirmModal content="Close this tab?" onConfirm={closeTab} refresh={showConfirmModal}/>
			}

			<div className={`tab ${isCurrTab ? 'active' : ''}`} onClick={switchTab}>
				<div/>

				<p>{tabName}</p>

				<button onClick={() => {setShowConfirmModal(true)}}>
					<Image src={closeBlack} alt="Close Icon" />
				</button>
			</div>
		</>
	)
}

export default Tab