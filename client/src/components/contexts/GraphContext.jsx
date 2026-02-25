'use client';

import React, { createContext, useState, useEffect } from 'react'


export const GraphContext = createContext();

export const GraphProvider = ({ allNodes, allLinks, children }) => {
	const [handTool, setHandTool] = useState(0);
	const [nodes, setNodes] = useState(allNodes || []);
	const [links, setLinks] = useState(allLinks || []);
	
	useEffect(() => {
		setNodes(allNodes || [])
	}, [allNodes])

	useEffect(() => {
		setLinks(allLinks || [])
	}, [allLinks])

	return (
		<GraphContext.Provider value={{ 
			handTool, setHandTool, 
			nodes, setNodes, 
			links, setLinks
		}}>
			{children}
		</GraphContext.Provider>
	)
}
