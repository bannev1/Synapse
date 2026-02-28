"use client"

import React, { useEffect, useState, useContext } from 'react'

import { GraphContext } from '@/components/contexts/GraphContext';


function PathFinderModal({
	refresh,
	updateRefresh,
	onSubmit
}) {
	const { selectedNode } = useContext(GraphContext)
	const [exists, setExists] = useState(refresh);
	
	useEffect(() => {
		setExists(refresh)
	}, [refresh])

	const handleFindPath = () => {
		if (selectedNode && selectedNode.group === 'source') {
			onSubmit(selectedNode.source)
			setExists(false)
		}
	}

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

						{
							selectedNode && selectedNode.group === 'source' ? (

							<>
								<p>Do you want to highlight the path for this node?</p>
								<input type="text" value={selectedNode?.source ?? ''} readOnly={true}/>
								<div className='buttons'>
									<button className="no" onClick={() => updateRefresh()}>No</button>
									<button className="yes" onClick={handleFindPath}>Yes</button>
								</div>
							</>

						) : ( // For when no node is selected 
							<>
								<p>Please select a source node by right-clicking it first before finding its path.</p>
								<div className='buttons'>
									<button onClick={() => updateRefresh()}>Close</button>
								</div>
							</>
						)}
					</div>
				</>
			}
		</>
	)
}

export default PathFinderModal
