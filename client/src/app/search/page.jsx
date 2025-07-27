'use client';

import React, { useContext, useState } from 'react'

import SearchBar from '@/components/SearchBar'
import TabBar from '@/components/TabBar';
import '../../styles/search/styles.css'
import { TabContext } from '@/components/TabContext';
import ConfirmModal from '@/components/modals/ConfirmModal';
import SearchOptions from '@/components/SearchOptions';

function Search() {
  const {tabs, setTabs} = useContext(TabContext)
  
  const tabsExist = tabs.length > 0 // If tabs, then show tab bar
  const inverted = tabsExist ? '' : 'inverted'

  const [searchOptions, setSearchOptions] = useState({})

  return (
    <>
      { // Tab viewer
        tabsExist && 
        <TabBar currTab='' isNewTab={true}/>
      }

      {/* Main content */}
      <div id="home" className={inverted}>
        <div style={{'position': 'relative'}}>
          <h1 className={`underline blue ${inverted}`}>Synapse</h1>
          <p id="slogan">Think connected.</p>
        </div>

        <SearchBar inverted={tabsExist} placeholder="What's your next search?" height={25}/>

        <SearchOptions onChangeOptions={setSearchOptions} inverted={!tabsExist}/>
      </div>
    </>
  )
}

export default Search