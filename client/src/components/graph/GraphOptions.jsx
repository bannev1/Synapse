'use client'

import React, { useContext, useState } from 'react'
import Image from 'next/image'
import { useRouter } from 'next/navigation'

// Components
import AddNodeModal from '../modals/graphFunctions/AddNodeModal'
import DeleteNodeModal from '../modals/graphFunctions/DeleteNodeModal'
import PathFinderModal from '../modals/graphFunctions/PathFinderModal'
import Loading from '../Loading'
import ErrorModal from '../modals/ErrorModal'
import SaveGraphModal from '../modals/graphFunctions/SaveGraphModal'

import { GraphContext } from '../contexts/GraphContext'
import { TabContext } from '../contexts/TabContext'
import { addNode, deleteNode, findPath } from '@/scripts/search'
import { uploadGraph } from '@/scripts/save'

// Icons
import appsWhite from '/public/icons/appsWhite.svg'
import closeWhite from '/public/icons/closeWhite.svg'
import saveBlack from '/public/icons/saveBlack.svg'
import nodeAddWhite from '/public/icons/nodeAddWhite.svg'
import deleteWhite from '/public/icons/deleteWhite.svg'
import pathWhite from '/public/icons/pathWhite.svg'


function GraphOptions({ tabName, canSave = true }) {
	const { tabs, setTabs } = useContext(TabContext)
	const { rawGraph, updateProvidedGraph, setHighlightNodes } = useContext(GraphContext)
	
	const router = useRouter()

	const [opened, setOpened] = useState(false);
	// 0 means no modal, 1 means add, 2 means delete, 3 means path finder, 4 means save
	const [currentModal, setCurrentModal] = useState(0)
	
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState(false)


	// Close modal
	const closeModal = () => {
		setCurrentModal(0)
	}

	// Add Node
	const addNodeHandler = async (source, topic = null) => {
		setLoading(true) // Show loading

		// Call API to add node to current graph
		const updatedGraph = await addNode(rawGraph, source, topic)
		
		if (updatedGraph === 'error') {
			console.log(updatedGraph)
			setError(true)
			setLoading(false)
		}
		
		// Update graph context
		updateProvidedGraph(updatedGraph)

		// Update the current tab with the new graph
		if (tabName != '') {
			const updatedTabs = tabs.map(tab => {
				if (tab.name === tabName)
					return {
						...tab,
						graph: updatedGraph
					}
	
				return tab
			})
	
			// Update tabs in context
			setTabs(updatedTabs)
		}

		// Close modal
		setCurrentModal(0)
		setLoading(false)
	}


	// Delete Node
	const deleteNodeHandler = async (source) => {
		setLoading(true) // Show loading

		// Call API to delete node from current graph
		const updatedGraph = await deleteNode(rawGraph, source)
		
		if (updatedGraph === 'error') {
			console.log(updatedGraph)
			setError(true)
			setLoading(false)
		}
		
		// Update graph context
		updateProvidedGraph(updatedGraph)

		// Update the current tab with the new graph
		if (tabName != '') {
			const updatedTabs = tabs.map(tab => {
				if (tab.name === tabName)
					return {
						...tab,
						graph: updatedGraph
					}
	
				return tab
			})
	
			// Update tabs in context
			setTabs(updatedTabs)
		}

		// Close modal
		setCurrentModal(0)
		setLoading(false)
	}


	// Find Path of Node
	const findPathHandler = async (source) => {
		setLoading(true) // Show loading

		// Call API to get path
		const path = await findPath(rawGraph, source)
		
		if (path === 'error') {
			console.log(path)
			setError(true)
			setLoading(false)
		}

		// Highlight path
		setHighlightNodes(path)

		// Close modal
		setCurrentModal(0)
		setLoading(false)
	}


	// Save Graph
	const saveGraphHandler = async (newName) => {
		setLoading(true)

		const updatedGraph = { 
			...rawGraph, 
			name: newName 
		}

		// Save
		const result = await uploadGraph(updatedGraph)

		if (result === 'error') {
			setError(true)
			setLoading(false)
			return
		}

		// Redirect to saved graph site
		router.push(`/load/${result}`)
	}


	return (
		<>
			<button onClick={() => setOpened(true)} id="options">
				<Image src={appsWhite} alt='Apps Icon'/>
			</button>

			{ opened &&
				<>
					<div id='optionsModal' className='popup'>
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
							<button onClick={() => {
								setOpened(false)
								setCurrentModal(0)
							}}>
								<Image src={closeWhite} alt='Close Icon'/>
							</button>

							{ // Only if can save
								canSave &&
								<button className='active' onClick={() => setCurrentModal(4)}>
									<Image src={saveBlack} alt='Save Icon'/>
								</button>
							}
						</div>
					</div>

					{/* Modals */}
					<AddNodeModal refresh={currentModal == 1} onSubmit={addNodeHandler} updateRefresh={closeModal}/>
					<DeleteNodeModal refresh={currentModal == 2} onSubmit={deleteNodeHandler} updateRefresh={closeModal}/>
					<PathFinderModal refresh={currentModal == 3} onSubmit={findPathHandler} updateRefresh={closeModal}/>
					<SaveGraphModal refresh={currentModal == 4} onSubmit={saveGraphHandler} updateRefresh={closeModal}/>

					
					{ // Loading
						loading && 
						<Loading/>
					}

					{/* Error Modal */}
					<ErrorModal content={'Error completing graph operation. Please try again.'} refresh={error}/>
				</>
			}
		</>
	)
}

export default GraphOptions