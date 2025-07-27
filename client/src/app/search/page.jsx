'use client';

import React, { useContext } from 'react'

import SearchBar from '@/components/SearchBar'
import TabBar from '@/components/TabBar';
import '../../styles/search/styles.css'
import { TabContext } from '@/components/TabContext';
import ConfirmModal from '@/components/modals/ConfirmModal';

function Search() {
  const {tabs, setTabs} = useContext(TabContext)
  
  const tabsExist = tabs.length >= 0 // If tabs, then show tab bar
  const inverted = tabsExist ? '' : 'inverted'

  return (
    <>
      { // Tab viewer
        tabsExist && 
        <TabBar/>
      }

      {/* Main content */}
      <div id="home" className={inverted}>
        <div style={{'position': 'relative'}}>
          <h1 className={`underline blue ${inverted}`}>Synapse</h1>
          <p id="slogan">Think connected.</p>
        </div>

        <SearchBar inverted={tabsExist} placeholder="What's your next search?" height={25}/>

        <div id="options">

        </div>

        <ConfirmModal content="Confirm?"/>
      </div>
    </>
  )
}

export default Search