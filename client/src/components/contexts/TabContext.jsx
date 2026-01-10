'use client';

import React, { createContext, useState } from 'react'


export const TabContext = createContext();

export const TabProvider = ({ children }) => {
	const [tabs, setTabs] = useState([]);
	// Tab format obj:
	// {
	// 	'name': 'Tab Name',
	// 	'graph': 'GRAPH OBJ - see graphcontext'
	// }

	return (
		<TabContext.Provider value={{ tabs, setTabs }}>{children}</TabContext.Provider>
	)
}
