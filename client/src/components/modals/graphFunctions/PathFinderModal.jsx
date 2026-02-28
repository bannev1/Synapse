"use client"

import React, { useEffect, useState } from 'react'


function PathFinderModal({
	refresh,
	updateRefresh,
	onSubmit
}) {
	const [exists, setExists] = useState(refresh);
	
	useEffect(() => {
		setExists(refresh)
	}, [refresh])

	return (
		<>
			{
				exists &&
				<>
					<div className='modalBackdrop' onClick={() => {
						updateRefresh()
					}}/>

					<div className='modal'>
						<h1>Find Path of Node</h1>

						<div className='buttons'>
							<button onClick={() => onSubmit()}>Close</button>
						</div>
					</div>
				</>
			}
		</>
	)
}

export default PathFinderModal
