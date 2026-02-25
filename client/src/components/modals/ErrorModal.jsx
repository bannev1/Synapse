import React, { useEffect, useState } from 'react'


function ErrorModal({
	content,
	refresh
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
						<h1>Error</h1>
						<p>{content}</p>

						<div className='buttons'>
							<button>Close</button>
						</div>
					</div>
				</>
			}
		</>
	)
}

export default ErrorModal
