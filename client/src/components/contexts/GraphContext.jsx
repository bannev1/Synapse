'use client';

import React, { createContext, useState } from 'react'


export const GraphContext = createContext();

export const GraphProvider = ({ children }) => {
	const [handTool, setHandTool] = useState(0);

	return (
		<GraphContext.Provider value={{ handTool, setHandTool }}>{children}</GraphContext.Provider>
	)
}
