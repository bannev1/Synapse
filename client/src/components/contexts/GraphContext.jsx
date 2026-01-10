'use client';

import React, { createContext, useState } from 'react'


export const GraphContext = createContext();

export const GraphProvider = ({ allNodes, allLinks, children }) => {
	const [handTool, setHandTool] = useState(0);
	const [nodes, setNodes] = useState(allNodes);
	const [links, setLinks] = useState(allLinks);
	// const [comments, setComments] = useState(allComments); // Future project

	return (
		<GraphContext.Provider value={{ handTool, setHandTool, nodes, setNodes, links, setLinks }}>{children}</GraphContext.Provider>
	)
}
