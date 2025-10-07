import React from 'react'

import { useState, useCallback } from 'react';

import ForceGraph2D from 'https://esm.sh/react-force-graph-2d?external=react';
import { CSS2DRenderer, CSS2DObject } from 'https://esm.sh/three/examples/jsm/renderers/CSS2DRenderer.js';

import { GraphProvider } from '@/components/contexts/GraphContext'

// Components
import GraphToolbar from './GraphToolbar';
import GraphOptions from './GraphOptions';


const extraRenderers = [new CSS2DRenderer()];


function GraphView() {
	return (
		<div id='graph'>
			<GraphProvider>
				{/* Force Graph 2D */}
				<ForceGraph3D
					extraRenderers={extraRenderers}
					graphData={data}
					nodeAutoColorBy="group"
					nodeThreeObject={node => {
						const nodeEl = document.createElement('div');
						nodeEl.textContent = node.id;
						nodeEl.className = 'node';
						return new CSS2DObject(nodeEl);
					}}
					nodeThreeObjectExtend={true}
				/>

				<GraphToolbar/>

				<GraphOptions/>
			</GraphProvider>
		</div>
	)
}

export default GraphView