'use client'

import React from 'react'

import '@/styles/view/styles.css'

import Search from '../page'

function ViewNewTab() { // New tab view
	return (
		<Search forceNewTabView={true}/>
	)
}

export default ViewNewTab