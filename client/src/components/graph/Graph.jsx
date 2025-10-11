'use client'

import React, { useContext } from 'react'

import { useState, useCallback } from 'react';

import ForceGraph2D from 'react-force-graph-2d';

import { GraphContext } from '@/components/contexts/GraphContext'

// Components
import GraphToolbar from './GraphToolbar';
import GraphOptions from './GraphOptions';


function Graph() {
	const {nodes, setNodes, links, setLinks} = useContext(GraphContext)


	return (
		<div id='graph'>
			<ForceGraph2D
				graphData={{
					"nodes": nodes,
					"links": links
				}}
				nodeAutoColorBy="group"
				nodeCanvasObject={(node, ctx, globalScale) => {
					const label = node.id;
					const fontSize = 12/globalScale;

					ctx.font = `${fontSize}px Sans-Serif`;

					const textWidth = ctx.measureText(label).width;
					const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

					ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
					ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);

					ctx.textAlign = 'center';
					ctx.textBaseline = 'middle';
					ctx.fillStyle = node.color;
					ctx.fillText(label, node.x, node.y);

					node.__bckgDimensions = bckgDimensions;
				}}
				nodePointerAreaPaint={(node, color, ctx) => {
					ctx.fillStyle = color;
					const bckgDimensions = node.__bckgDimensions;
					bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
				}}
			/>

			<GraphToolbar/>

			<GraphOptions/>
		</div>
	)
}

export default Graph
