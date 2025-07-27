import React, { useState } from 'react'
import Image from 'next/image';

import addBlack from '/public/icons/addBlack.svg';
import removeBlack from '/public/icons/removeBlack.svg';
import addWhite from '/public/icons/addWhite.svg';
import removeWhite from '/public/icons/removeWhite.svg';

function SearchOptions(
	onChangeOptions,
	inverted = false
) {
	return (
		<div id="searchOptions" className={inverted ? 'inverted' : ''}>
			<div id='sourcesSelect'>
				<select>
					<option>Test</option>
				</select>
			</div>

			<div id='depthSelect'>
				<button>
					<Image src={inverted ? addWhite : addBlack} alt='Add Icon' />
				</button>

				<label for='depthSelector'>Depth</label>
				<input type='text' name='depthSelector' defaultValue={6} onChange={() => {}}/>

				<button>
					<Image src={inverted ? removeWhite : removeBlack} alt='Remove Icon'/>
				</button>
			</div>
		</div>
  )
}

export default SearchOptions