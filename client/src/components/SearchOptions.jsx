import React, { useEffect, useState } from 'react'
import Image from 'next/image';

import addBlack from '/public/icons/addBlack.svg';
import removeBlack from '/public/icons/removeBlack.svg';
import addWhite from '/public/icons/addWhite.svg';
import removeWhite from '/public/icons/removeWhite.svg';

function SearchOptions({
	onChangeOptions,
	inverted = false
}) {
	const [depthVal, setDepthVal] = useState(6)
	const [sourceOptions, setSourceOptions] = useState([])

	useEffect(() => {
		onChangeOptions({
			'depth': depthVal,
			'sources': sourceOptions
		})
	}, [depthVal, sourceOptions])

	return (
		<div id="searchOptions" className={inverted ? 'inverted' : ''}>
			<div id='sourcesSelect'>
				<select>
					<option>Test</option>
				</select>
			</div>

			<div id='depthSelect'>
				<button onClick={() => {depthVal < 9 ? setDepthVal(depthVal+1) : setDepthVal(depthVal)}}>
					<Image src={inverted ? addWhite : addBlack} alt='Add Icon' />
				</button>

				<label htmlFor='depthSelector'>Depth</label>
				<input type='text' name='depthSelector' value={depthVal} onChange={(e) => {setDepthVal(e.target.value)}}/>

				<button onClick={() => {depthVal > 1 ? setDepthVal(depthVal-1) : setDepthVal(depthVal)}}>
					<Image src={inverted ? removeWhite : removeBlack} alt='Remove Icon'/>
				</button>
			</div>
		</div>
  )
}

export default SearchOptions