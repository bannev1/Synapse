"use client"

import React, { createContext, useState, useEffect } from "react"

export const TabContext = createContext()

export const TabProvider = ({ children }) => {
	const [tabs, setTabs] = useState([])
	const [isLoaded, setIsLoaded] = useState(false)

	// Load tabs from localStorage
	useEffect(() => {
		const storedTabs = localStorage.getItem('synapseTabs')
		
		if (storedTabs) {
			try {
				setTabs(JSON.parse(storedTabs))
			} catch (error) {
				localStorage.removeItem('synapseTabs')
			}
		}

		setIsLoaded(true)
	}, [])

	// Save tabs to localStorage
	useEffect(() => {
		if (isLoaded)
			localStorage.setItem('synapseTabs', JSON.stringify(tabs))
	}, [tabs, isLoaded])

	return (
		<TabContext.Provider value={{ tabs, setTabs }}>
			{children}
		</TabContext.Provider>
	)
}
