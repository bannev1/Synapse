import React, { useEffect, useState } from 'react'

function ConfirmModal({
	content,
	onConfirm,
	refresh,
	backdrop = true,
	inverted = false,
	noConfirmText = 'No',
	yesConfirmText = 'Yes'
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
					{
						backdrop &&
						<div className='modalBackdrop' onClick={() => {setExists(false)}}/>
					}

					<div className={`modal ${inverted ? 'inverted' : ''}`}>
						<h1>{content}</h1>
						<div className='divider'/>
						<div className='buttons'>
							<button className='no' onClick={() => {setExists(false)}}>{noConfirmText}</button>
							<button className='yes' onClick={onConfirm}>{yesConfirmText}</button>
						</div>
					</div>
				</>
			}
		</>
	)
}

export default ConfirmModal