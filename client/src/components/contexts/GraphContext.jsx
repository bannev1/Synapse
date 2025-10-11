'use client';

import React, { createContext, useState } from 'react'


export const GraphContext = createContext();

export const GraphProvider = ({ children }) => {
	const [handTool, setHandTool] = useState(0);
	const [nodes, setNodes] = useState([
		{ 
          "id": "id1",
		  "site": "NY Times",
		  "link": "https://nytimes.com/"
        },
	]);
	const [links, setLinks] = useState([]);

	return (
		<GraphContext.Provider value={{ handTool, setHandTool, nodes, setNodes, links, setLinks }}>{children}</GraphContext.Provider>
	)
}
