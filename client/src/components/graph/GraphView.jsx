import React from 'react'

import { useState, useCallback } from 'react';
import { ReactFlow, applyNodeChanges, applyEdgeChanges, addEdge } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import { GraphProvider } from '@/components/contexts/GraphContext'

// Components
import GraphToolbar from './GraphToolbar';
import GraphOptions from './GraphOptions';


function GraphView() {
	const [nodes, setNodes] = useState(initialNodes);
 	const [edges, setEdges] = useState(initialEdges);

	const onNodesChange = useCallback(
		(changes) => setNodes((nodesSnapshot) => applyNodeChanges(changes, nodesSnapshot)),
		[],
	);
	const onEdgesChange = useCallback(
		(changes) => setEdges((edgesSnapshot) => applyEdgeChanges(changes, edgesSnapshot)),
		[],
	);
	const onConnect = useCallback(
		(params) => setEdges((edgesSnapshot) => addEdge(params, edgesSnapshot)),
		[],
	);


	return (
		<div id='graph'>
			<GraphProvider>
				<ReactFlow
					nodes={nodes}
					edges={edges}
					onNodesChange={onNodesChange}
					onEdgesChange={onEdgesChange}
					onConnect={onConnect}
					colorMode='light'
					fitView
					/>

				<GraphToolbar/>

				<GraphOptions/>
			</GraphProvider>
		</div>
	)
}

export default GraphView