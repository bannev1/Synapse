'use client';

import autocomplete from '@/scripts/requests/autocomplete';
import React, { useEffect, useState } from 'react'

function Autocompleter({ query, setAutocomplete, maxOptions = 5, inverted = false }) {
	const [options, setOptions] = useState([])

	useEffect(() => {
		autocomplete(query, maxOptions).then((result) => {
			setOptions(result)
		})
	}, [])
	
	return (
		<div id="autocomplete" className={inverted ? 'inverted' : ''}>
			{
				options.forEach(option => {
					<li>
						<button onClick={() => {setAutocomplete(option)}}>
							{option}
						</button>
					</li>
				})
			}
		</div>
	)
}

export default Autocompleter