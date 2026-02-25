'use client';

import React, { createContext, useState, useEffect } from 'react'


export const GraphContext = createContext();

export const GraphProvider = ({ allNodes, allLinks, topics, children }) => {
	const [handTool, setHandTool] = useState(0);
	const [nodes, setNodes] = useState(allNodes || []);
	const [links, setLinks] = useState(allLinks || []);
	const [topics, setTopics] = useState(topics || []);
	
	useEffect(() => {
		setNodes(allNodes || [])
	}, [allNodes])

	useEffect(() => {
		setLinks(allLinks || [])
	}, [allLinks])

	useEffect(() => {
		setLinks(topics || [])
	}, [topics])

	return (
		<GraphContext.Provider value={{ 
			handTool, setHandTool, 
			nodes, setNodes, 
			links, setLinks, 
			topics, setTopics 
		}}>
			{children}
		</GraphContext.Provider>
	)
}
