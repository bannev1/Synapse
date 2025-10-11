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

	// Hover
	const [hoveredNode, setHoveredNode] = useState(null);

	// Return
	return (
		<div id='graph'>
			<ForceGraph2D
				ref={graphRef}
				graphData={{
					"nodes": nodes,
					"links": links
				}}
				nodeAutoColorBy="group"
				onNodeHover={node => setHoveredNode(node)}
				nodeCanvasObject={(node, ctx, globalScale) => {
					// Set up node
					const label = node.site;
					const fontSize = 16;
					const baseIconSize = 24;
					const iconSize = hoveredNode === node ? baseIconSize * 1.3 : baseIconSize;
					const iconSpacing = 8;
					const padding = fontSize * 0.8;

					ctx.font = `700 ${fontSize}px Montserrat, Sans-Serif`;
					ctx.fontWeight = '700';

					const textWidth = ctx.measureText(label).width;
					
					const bckgWidth = textWidth + baseIconSize + padding * 2 + iconSpacing;
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
					ctx.fillText(label, node.x - (fontSize + iconSpacing + baseIconSize/2) / 2, node.y);
					
					// Draw img once loaded
					if (blackOpenNewImg) {
						const iconX = node.x + (bckgWidth / 2) - (iconSize - (iconSize - baseIconSize)/2) - padding/2;
						const iconY = node.y - bckgHeight / 2 + (bckgHeight - (iconSize - (iconSize - baseIconSize)/2)) / 2;

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
					if (!blackOpenNewImg || !whiteOpenNewImg) {
						return;
					}

					const graphCoords = graphRef.current.screen2GraphCoords(event.clientX, event.clientY);
					if (node.__iconArea) {
						const ia = node.__iconArea;
						if (graphCoords.x >= ia.x && graphCoords.x <= ia.x + ia.width && 
							graphCoords.y >= -ia.y && graphCoords.y <= -ia.y + ia.height) {
							event.preventDefault();
							window.open(node.link, '_blank');
							return; 
						}
					}

					console.log('Node clicked:', node);
				}}
				onNodeDragEnd={node => {
					node.fx = node.x;
					node.fy = node.y;
					node.fz = node.z;
				}}
			/>

			<GraphToolbar/>

			<GraphOptions/>
		</div>
	)
}

export default Graph
