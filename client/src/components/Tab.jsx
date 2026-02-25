'use client';

import React, { useState } from 'react'
import Image from 'next/image'
import { redirect } from 'next/navigation';

import closeBlack from '/public/icons/closeBlack.svg'
import ConfirmModal from './modals/ConfirmModal';

function Tab({
	index,
	tabName,
	graph,
	onDelete,
	isCurrTab = false,
	isNewTab = false,
}) {
	if (graph == undefined && !isCurrTab)
		return

	const [showConfirmModal, setShowConfirmModal] = useState(false)


	const closeTab = () => {
		if (!isCurrTab) {
			onDelete()
		}
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

				<p className={isNewTab ? 'newTab' : ''}>{isNewTab ? 'New Tab' : tabName}</p>

				{
					!isCurrTab && // So can't close current or new tabs

					<button onClick={() => {setShowConfirmModal(true)}}>
						<Image src={closeBlack} alt="Close Icon" />
					</button>
				}
			</div>
		</>
	)
}

export default Tab