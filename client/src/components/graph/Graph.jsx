'use client'

import React, { useContext, useRef, useState, useEffect } from 'react'
import ForceGraph2D from 'react-force-graph-2d';

import { GraphContext } from '@/components/contexts/GraphContext'

// Components
import GraphToolbar from './GraphToolbar';
import GraphOptions from './GraphOptions';


function Graph() {
	const {nodes, setNodes, links, setLinks} = useContext(GraphContext)
	const graphRef = useRef();

	// Set up Images
	const [whiteOpenNewImg, setWhiteOpenNewImg] = useState(null);
	const [blackOpenNewImg, setBlackOpenNewImg] = useState(null);
	
	useEffect(() => {
		const imgWhite = new Image();
		imgWhite.src = '/icons/openInNewWhite.svg';
		imgWhite.onload = () => setWhiteOpenNewImg(imgWhite);

		const imgBlack = new Image();
		imgBlack.src = '/icons/openInNewBlack.svg';
		imgBlack.onload = () => setBlackOpenNewImg(imgBlack);
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
					const iconSize = 24;
					const iconSpacing = 8;
					const padding = fontSize * 0.8;

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
					ctx.fillText(label, node.x - (fontSize + iconSpacing + iconSize/2) / 2, node.y);
					
					// Draw img once loaded
					if (blackOpenNewImg) {
						const iconX = node.x + (bckgWidth / 2) - iconSize - padding/2;
						const iconY = node.y - iconSize / 2;

						ctx.drawImage(blackOpenNewImg, iconX, iconY, iconSize, iconSize);

						node.__iconArea = { x: iconX, y: iconY, width: iconSize, height: iconSize };
					}
				}}
				nodePointerAreaPaint={(node, color, ctx) => {
					ctx.fillStyle = color;
					const bckgDimensions = node.__bckgDimensions;
					bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
				}}
				onNodeClick={(node, event) => {
					const graphCoords = graphRef.current.screen2GraphCoords(event.clientX, event.clientY);
					
					if (node.__iconArea) {
						const ia = node.__iconArea;
						if (graphCoords.x >= ia.x && graphCoords.x <= ia.x + ia.width && 
							graphCoords.y >= ia.y && graphCoords.y <= ia.y + ia.height) {
							console.log('Icon clicked for node:', node);
							return; 
						}
					}

					console.log('Node clicked:', node);
				}}
			/>

			<GraphToolbar/>

			<GraphOptions/>
		</div>
	)
}

export default Graph
