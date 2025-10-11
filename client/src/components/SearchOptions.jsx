'use client'

import React, { useEffect, useRef, useState } from 'react'
import Image from 'next/image';

import addBlack from '/public/icons/addBlack.svg';
import removeBlack from '/public/icons/removeBlack.svg';
import addWhite from '/public/icons/addWhite.svg';
import removeWhite from '/public/icons/removeWhite.svg';
import dropdownWhite from '/public/icons/dropdownWhite.svg';
import dropdownBlack from '/public/icons/dropdownBlack.svg';

function SearchOptions({
	onChangeOptions,
	inverted = false
}) {
	const [depthVal, setDepthVal] = useState(6)
	const [sourceOptions, setSourceOptions] = useState([])
	const [showSources, setShowSources] = useState(false)
	const [useAllSource, setUseAllSource] = useState(true)

	useEffect(() => {
		onChangeOptions({
			'depth': depthVal,
			'sources': sourceOptions,
			'useAll': useAllSource
		})
	}, [depthVal, sourceOptions, useAllSource])

	const allSources = useRef([
		['https://www.wikipedia.com/', 'Wikipedia'],
		["https://www.nytimes.com/", 'New York Times'],
		["https://www.youtube.com", 'YouTube'],
		["https://www.bbc.com/", 'BBC News'],
		["https://www.researchgate.net/", 'ResearchGate'],
		["https://medium.com/", 'Medium'],
		["https://arxiv.org/", 'ArXiv'],
		["https://edition.cnn.com/", 'CNN'],
		["https://www.ft.com/", 'Financial Times'],
		["https://www.sciencedirect.com/", 'ScienceDirect'],
		["https://www.britannica.com/", 'Britannica'],
	]).current

	return (
		<div id="searchOptions" className={inverted ? 'inverted' : ''}>
			<div id='sourcesSelect'>
				<div id="sourcesDropdownTitle" className={showSources ? 'active' : ''} onClick={() => setShowSources(v => !v)}>
					{
						useAllSource ?
						<p>Using Any Source</p> :
						<p>{sourceOptions.length} Sources Selected</p>
					}
					<Image src={inverted ? dropdownBlack : dropdownWhite} alt="Dropdown Icon"/>
				</div>

				{ showSources &&
					<div id="options">
						{
							allSources.map(([link, name], index) => {
								return <div key={index} className={`option ${sourceOptions.includes(link) ? 'active' : ''}`} 
											onClick={() => {
												setSourceOptions(v => {
													if (!v.includes(link))
														return [...v, link]
													else (v.includes(link))
														return v.filter(val => {return val != link})
												})
											}}>

											<label className={sourceOptions.includes(link) ? 'active' : ''}/>

											<p>{name}</p>
										</div>
							})
						}

						<div className="useAll" onClick={() => setUseAllSource(v => !v)}>
							<label className={useAllSource ? 'active' : ''}/>
							<p>Use Any Source</p>
						</div>
					</div>
				}
			</div>

			<div id='depthSelect'>
				<button onClick={() => setDepthVal(v => Math.min(9, v + 1))}>
					<Image src={inverted ? addBlack : addWhite} alt='Add Icon' />
				</button>

				<label htmlFor='depthSelector'>Depth</label>
				<input type='text' name='depthSelector' value={depthVal} readOnly/>

				<button onClick={() => setDepthVal(v => Math.max(1, v - 1))}>
					<Image src={inverted ? removeBlack : removeWhite} alt='Remove Icon'/>
				</button>
			</div>
		</div>
  )
}

export default SearchOptions