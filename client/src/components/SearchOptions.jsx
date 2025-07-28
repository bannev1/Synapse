import React, { useEffect, useState } from 'react'
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

	useEffect(() => {
		onChangeOptions({
			'depth': depthVal,
			'sources': sourceOptions
		})
	}, [depthVal, sourceOptions])

	return (
		<div id="searchOptions" className={inverted ? 'inverted' : ''}>
			<div id='sourcesSelect'>
				<div>
					<p>{sourceOptions.length} Sources Selected</p>
					<Image src={inverted ? dropdownWhite : dropdownBlack} alt="Dropdown Icon"/>
				</div>

				<select multiple>
					<option value="https://www.wikipedia.org/">Wikipedia</option>
					<option value="https://www.nytimes.com/">The New York Times</option>
					<option value="https://www.youtube.com">YouTube</option>
					<option value="https://www.bbc.com/">BBC</option>
					<option value="https://www.researchgate.net/">ResearchGate</option>
					<option value="https://medium.com/">Medium</option>
					<option value="https://arxiv.org/">ArXiv</option>
					<option value="https://edition.cnn.com/">CNN</option>
					<option value="https://www.ft.com/">Financial Times</option>
					<option value="https://www.sciencedirect.com/">Science Direct</option>
					<option value="https://www.britannica.com/">Britannica</option>
				</select>
			</div>

			<div id='depthSelect'>
				<button onClick={() => {depthVal < 9 ? setDepthVal(depthVal+1) : setDepthVal(depthVal)}}>
					<Image src={inverted ? addWhite : addBlack} alt='Add Icon' />
				</button>

				<label htmlFor='depthSelector'>Depth</label>
				<input type='text' name='depthSelector' value={depthVal} 
						onInput={(event) => {
							if (!/[0-9]/.test(event.key)) {
								event.preventDefault();
							}
						}}/>

				<button onClick={() => {depthVal > 1 ? setDepthVal(depthVal-1) : setDepthVal(depthVal)}}>
					<Image src={inverted ? removeWhite : removeBlack} alt='Remove Icon'/>
				</button>
			</div>
		</div>
  )
}

export default SearchOptions