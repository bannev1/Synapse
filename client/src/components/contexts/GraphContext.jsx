'use client';

import React, { createContext, useState, useEffect } from 'react'


export const GraphContext = createContext();

export const GraphProvider = ({ allNodes, allLinks, topics: allTopics, children }) => {
	const [handTool, setHandTool] = useState(0);
	const [nodes, setNodes] = useState(allNodes || []);
	const [links, setLinks] = useState(allLinks || []);
	const [topics, setTopics] = useState(allTopics || []);
	
	useEffect(() => {
		setNodes(allNodes || [])
	}, [allNodes])

	useEffect(() => {
		setLinks(allLinks || [])
	}, [allLinks])

	useEffect(() => {
		setTopics(allTopics || [])
	}, [allTopics])

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
