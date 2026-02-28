"use client"

import React, { useEffect, useState } from 'react'


function SaveGraphModal({
	refresh,
	updateRefresh,
	onSubmit
}) {
	const [exists, setExists] = useState(refresh)
	const [graphName, setGraphName] = useState('')

	useEffect(() => {
		setExists(refresh)

		if (refresh)
			setGraphName('')
	}, [refresh])

	const handleClose = () => {
		setExists(false)
	}

	return (
		<>
			{
				exists &&
				<>
					<div className='modalBackdrop' onClick={() => {
						setExists(false)
						updateRefresh()
					}}/>

					<div className='modal'>
						<h1>Save Graph</h1>

						<label>Graph Name:</label>
						<input type="text" onChange={(e) => setGraphName(e.target.value)} placeholder="Enter graph name"/>

						<div className='buttons'>
							<button onClick={handleClose}>Close</button>
							<button onClick={() => {onSubmit(graphName)}}>Upload</button>
						</div>
					</div>
				</>
			}
		</>
	)
}

export default SaveGraphModal
