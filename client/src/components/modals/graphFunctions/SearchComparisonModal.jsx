"use client"

import React, { useEffect, useState } from 'react'


function SearchComparisonModal({
	refresh,
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
					<div className='modalBackdrop' onClick={() => {setExists(false)}}/>

					<div className='modal'>
						<h1>Create Compare Graph</h1>

						<div className='buttons'>
							<button>Close</button>
						</div>
					</div>
				</>
			}
		</>
	)
}

export default SearchComparisonModal
