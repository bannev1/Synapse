"use client"

import React, { useEffect, useState, useContext } from 'react'

import { GraphContext } from '@/components/contexts/GraphContext';


function DeleteNodeModal({
	refresh,
	updateRefresh,
	onSubmit
}) {
	const { selectedNode, setSelectedNode } = useContext(GraphContext)
	const [exists, setExists] = useState(refresh);
	
	useEffect(() => {
		setExists(refresh)
	}, [refresh])

	const handleDelete = () => {
		if (selectedNode) {
			onSubmit(selectedNode.source)
			setSelectedNode(null) // Clear selection after deletion
			setExists(false)
		}
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
						<h1>Delete Node</h1>

						{
							selectedNode ? (

							<>
								<p>Do you want to delete this node?</p>
								<input type="text" value={selectedNode?.source ?? ''} readOnly={true}/>
								<div className='buttons'>
									<button className="no" onClick={() => setExists(false)}>No</button>
									<button className="yes" onClick={handleDelete}>Yes</button>
								</div>
							</>

						) : ( // For when no node is selected 
							<>
								<p>Please select a source node by right-clicking it first before deleting it.</p>
								<div className='buttons'>
									<button onClick={() => setExists(false)}>Close</button>
								</div>
							</>
						)}
					</div>
				</>
			}
		</>
	)
}

export default DeleteNodeModal
