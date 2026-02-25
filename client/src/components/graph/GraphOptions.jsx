'use client'

import React, { useState } from 'react'
import Image from 'next/image'

// Components
import AddNodeModal from '../modals/graphFunctions/AddNodeModal'
import DeleteNodeModal from '../modals/graphFunctions/DeleteNodeModal'
import PathFinderModal from '../modals/graphFunctions/PathFinderModal'

// Icons
import searchBlack from '/public/icons/searchBlack.svg'
import sendWhite from '/public/icons/sendWhite.svg'
import appsWhite from '/public/icons/appsWhite.svg'
import closeWhite from '/public/icons/closeWhite.svg'
import saveBlack from '/public/icons/saveBlack.svg'
import nodeAddWhite from '/public/icons/nodeAddWhite.svg'
import deleteWhite from '/public/icons/deleteWhite.svg'
import pathWhite from '/public/icons/pathWhite.svg'


function GraphOptions() {
	const [opened, setOpened] = useState(false);
	const [currentModal, setCurrentModal] = useState(0) // 0 means no modal, 1 means source, 2 means note, 3 means path finder


	// Add Node
	const addNode = (source) => {

	}


	// Delete Node
	const deleteNode = (source) => {

	}


	// Find Path of Node
	const findPath = (source) => {

	}


	return (
		<>
			<button onClick={() => setOpened(true)} id="options">
				<Image src={appsWhite} alt='Apps Icon'/>
			</button>

			{ opened &&
				<>
					<div id='optionsModal' className='popup'>
						{/* Search bar */}
						<div className='graphSearch'>
							<Image src={searchBlack} alt='Search Icon'/>

							<input type='text' placeholder='Graph Search...'/>

							<button>
								<Image src={sendWhite} alt='Send Icon'/>
							</button>
						</div>

						{/* Buttons */}
						<div className='graphOptions'>
							<button onClick={() => setCurrentModal(1)}>
								<Image src={nodeAddWhite} alt='Add Node Icon'/>
								<span>Add Node</span>
							</button>
							
							<button onClick={() => setCurrentModal(2)}>
								<Image src={deleteWhite} alt='Delete Node Icon'/>
								<span>Delete Node</span>
							</button>
							
							<button onClick={() => setCurrentModal(3)}>
								<Image src={pathWhite} alt='Path Finder Icon'/>
								<span>Find Path</span>
							</button>
						</div>

						{/* Close and save buttons */}
						<div className='optionModalButtons'>
							<button onClick={() => setOpened(false)}>
								<Image src={closeWhite} alt='Close Icon'/>
							</button>

							<button className='active'>
								<Image src={saveBlack} alt='Save Icon'/>
							</button>
						</div>
					</div>

					{/* Modals */}
					<AddNodeModal refresh={currentModal == 1} onSubmit={addNode}/>
					<DeleteNodeModal refresh={currentModal == 2} onSubmit={deleteNode}/>
					<PathFinderModal refresh={currentModal == 3} onSubmit={findPath}/>
				</>
			}
		</>
	)
}

export default GraphOptions