'use client';

import React, { useState } from 'react'
import Image from 'next/image'

import { search } from '@/scripts/requests/processor';

// Icons
import searchBlack from '/public/icons/searchBlack.svg';
import searchWhite from '/public/icons/searchWhite.svg';
import sendWhite from '/public/icons/sendWhite.svg';


function SearchBar({
	onSearch = search,
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

	return (
		<div 
			id="search" 
			className={inverted ? 'inverted' : ''} 
			style={styles}
		>
			{/* Search icon */}
			<Image src={inverted ? searchWhite : searchBlack} alt="Search Icon"/>
			
			{/* Input field */}
			<input type="text" placeholder={placeholder} className={(editable ? '' : 'notEditable') + (isPlaceholder ? 'placeholder' : '')}/>
			
			{/* Send button/search (only when editable) */}
			{
				editable &&

				<button onClick={onSearch}>
					<Image src={sendWhite} alt="Submit Icon"/>
				</button>
			}
		</div>
	)
}

export default SearchBar