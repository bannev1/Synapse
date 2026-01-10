'use client'

import React from 'react'

import '@/styles/view/styles.css'

import TabBar from '@/components/TabBar'
import Search from '../page'

function ViewNewTab() { // New tab view
	return (
		<TabBar isNewTab={true}/>
	)
}

export default ViewNewTab