'use client'

import React, { useContext, useRef, useState, useEffect } from 'react'
import ForceGraph2D from 'react-force-graph-2d';

import { GraphContext } from '@/components/contexts/GraphContext'

// Components
import GraphToolbar from './GraphToolbar';
import GraphOptions from './GraphOptions';

// Icons
import openInNewWhite from '/public/icons/openInNewWhite.svg';
import openInNewBlack from '/public/icons/openInNewBlack.svg';


function Graph() {
	const {nodes, setNodes, links, setLinks} = useContext(GraphContext)
	const graphRef = useRef();

	// Set up Images
	const [iconImage, setIconImage] = useState(null);
	
	useEffect(() => {
		const img = new Image();
		img.src = openInNewBlack;
		img.onload = () => setIconImage(img);
	}, []);

	return (
		<div id='graph'>
			<ForceGraph2D
				ref={graphRef}
				graphData={{
					"nodes": nodes,
					"links": links
				}}
				nodeAutoColorBy="group"
				nodeCanvasObject={(node, ctx, globalScale) => {
					// Set up node
					const label = node.site;
					const fontSize = 16;
					const iconSize = 16;
					const iconSpacing = 8;
					const padding = fontSize * 0.75;

					ctx.font = `700 ${fontSize}px Montserrat, Sans-Serif`;
					ctx.fontWeight = '700';

					const textWidth = ctx.measureText(label).width;
					
					const bckgWidth = textWidth + iconSize + padding * 2 + iconSpacing;
					const bckgHeight = fontSize + padding * 2;
					const bckgDimensions = [bckgWidth, bckgHeight];
					node.__bckgDimensions = bckgDimensions;


					
					ctx.fillStyle = node.color;
					const borderRadius = 5;
					ctx.beginPath();
					ctx.roundRect(
						node.x - bckgDimensions[0] / 2,
						node.y - bckgDimensions[1] / 2,
						bckgDimensions[0],
						bckgDimensions[1],
						borderRadius
						);
					ctx.fill();
					
					ctx.textAlign = 'center';
					ctx.textBaseline = 'middle';
					ctx.fillStyle = 'rgb(0, 0, 0)';
					ctx.fillText(label, node.x - (fontSize + iconSpacing) / 2, node.y);

					
					// Draw img once loaded
					if (iconImage) {
						const iconX = node.x + (bckgWidth / 2) - iconSize - padding/2;
						const iconY = node.y - iconSize / 2;

						ctx.drawImage(iconImage, iconX, iconY, iconSize, iconSize);

						node.__iconPos = { x: iconX, y: iconY, width: iconSize, height: iconSize };
					}
				}}
				nodePointerAreaPaint={(node, color, ctx) => {
					ctx.fillStyle = color;
					const bckgDimensions = node.__bckgDimensions;
					bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
				}}
				onNodeClick={(node, event) => {
					const rect = graphRef.current.getBoundingClientRect()
					const x = event.clientX - rect.left
					const y = event.clientY - rect.top
					
					if (node.__iconArea && 
						x >= node.__iconArea.x && 
						x <= node.__iconArea.x + node.__iconArea.width &&
						y >= node.__iconArea.y && 
						y <= node.__iconArea.y + node.__iconArea.height) {
						console.log('Icon clicked for node:', node)
						// Handle icon click
					} else {
						console.log('Node clicked:', node)
						// Handle node click
					}
				}}
			/>

			<GraphToolbar/>

			<GraphOptions/>
		</div>
	)
}

export default Graph
