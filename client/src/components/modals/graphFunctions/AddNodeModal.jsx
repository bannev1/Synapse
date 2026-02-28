"use client"

import React, { useEffect, useState, useContext } from 'react'

import { GraphContext } from '@/components/contexts/GraphContext';


function AddNodeModal({
	refresh,
	updateRefresh,
	onSubmit
}) {
	const { rawGraph } = useContext(GraphContext)
	const [exists, setExists] = useState(refresh);
	const [url, setUrl] = useState('')
	const [selectedTopic, setSelectedTopic] = useState('')
	const [errorMessage, setErrorMessage] = useState('')

	useEffect(() => {
		setExists(refresh)
		if (refresh && rawGraph?.topics?.length > 0) {
			setSelectedTopic(rawGraph.topics[0]) // Default to first topic if available
		}
	}, [refresh, rawGraph])

	const handleSubmit = (e) => {
		e.preventDefault()
		setErrorMessage('')

		// Validate URL
		try {
			new URL(url)
		} catch {
			setErrorMessage('Please enter a valid URL.')
			return
		}

		// Only proceed if topical graph and topic selected
		if (rawGraph.type === 'topical') {
			if (!selectedTopic) {
				setErrorMessage('Please select a topic.')
				return
			}
			onSubmit(url, selectedTopic)
		} else {
			// For non-topical, add without topic (as per original)
			onSubmit(url)
		}

		// Reset form and close modal
		setUrl('')
		setSelectedTopic('')
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
						<h1>Add Node</h1>

						<form onSubmit={handleSubmit} style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '10px' }}>
							<p>Enter URL of node to add:</p>
							<input type="text" placeholder="Enter valid URL" value={url} onChange={(e) => setUrl(e.target.value)} required />

							{
								// Dropdown only for topical graphs
								rawGraph.type === 'topical' && rawGraph?.topics?.length > 0 && (

								<>
									<p>Select topic to add node to:</p>

									<select value={selectedTopic} onChange={(e) => setSelectedTopic(e.target.value)} required>
										<option value="">Select a topic</option>
										{rawGraph.topics.map((topic) => (
											<option key={topic} value={topic}>
												{topic}
											</option>
										))}
									</select>
								</>
							)}

							{ 
								errorMessage && 
								<p style={{ color: 'red', margin: 0 }}>{errorMessage}</p>
							}

							<div className='buttons'>
								<button type="button" onClick={() => setExists(false)}>Close</button>
								<button type="submit">Add</button>
							</div>
						</form>
					</div>
				</>
			}
		</>
	)
}

export default AddNodeModal
