'use client';

import React, { useState } from 'react'
import Image from 'next/image'

// Icons
import searchBlack from '/public/icons/searchBlack.svg';
import searchWhite from '/public/icons/searchWhite.svg';
import sendWhite from '/public/icons/sendWhite.svg';


function SearchBar({
	onSearch,
	placeholder = 'Search',
	isPlaceholder = true, // If to use fancy styling for placeholder or not (otherwise placeholder looks like inputted text)
	inverted = false,
	minwidth = 300,
	maxwidth = 500,
	height = 25,
	editable = true
}) {
	const styles = {
		'--search-minwidth': `${minwidth}px`,
		'--search-maxwidth': `${maxwidth}px`,
		'--search-height': `${height}px`
	}

	const [query, setQuery] = useState('')

	const handleSearch = () => {
		onSearch(query)
		setQuery('')
	};

	const handleKeyDown = (e) => {
		if (e.key === 'Enter') {
			handleSearch()
		}
	}

	return (
		<div 
			id="search" 
			className={inverted ? 'inverted' : ''} 
			style={styles}
		>
			{/* Search icon */}
			<Image src={inverted ? searchWhite : searchBlack} alt="Search Icon"/>
			
			{/* Input field */}
			<input 
				type="text" 
				placeholder={placeholder} 
				className={(editable ? '' : 'notEditable') + (isPlaceholder ? 'placeholder' : '')} 
				readOnly={!editable}
				value={query}
				onChange={(e) => setQuery(e.target.value)}
				onKeyDown={handleKeyDown}
			/>
			
			{/* Send button/search (only when editable) */}
			{
				editable &&

				<button onClick={handleSearch}>
					<Image src={sendWhite} alt="Submit Icon"/>
				</button>
			}
		</div>
	)
}

export default SearchBar
