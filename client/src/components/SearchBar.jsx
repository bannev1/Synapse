'use client';

import React from 'react'
import Image from 'next/image'

import { search } from '@/scripts/requests/processor';

// Icons
import searchBlack from '/public/icons/searchBlack.svg';
import searchWhite from '/public/icons/searchWhite.svg';
import sendWhite from '/public/icons/sendWhite.svg';


function SearchBar({
  onSearch = search,
  placeholder = 'Search',
  inverted = false,
  minwidth = 300,
  maxwidth = 500,
  height = 25,
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
      <Image src={inverted ? searchWhite : searchBlack} alt="Search Icon"/>
      <input type="text" placeholder={placeholder}/>
      <button onClick={onSearch}>
        <Image src={sendWhite} alt="Submit Icon"/>
      </button>
    </div>
  )
}

export default SearchBar