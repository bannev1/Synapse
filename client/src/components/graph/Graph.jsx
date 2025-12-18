"use client"

import { useContext, useRef, useState, useEffect } from "react"
import ForceGraph from "react-force-graph-2d"

import { GraphContext } from "@/components/contexts/GraphContext"
import { generateNodeColor } from "@/scripts/colorSystem"

// Components
import GraphToolbar from "./GraphToolbar"
import GraphOptions from "./GraphOptions"

function Graph() {
  const { nodes, links, graphView } = useContext(GraphContext)
  const graphRef = useRef(null)
  const graphContainerRef = useRef(null)

  // Set up Images
  const [whiteOpenNewImg, setWhiteOpenNewImg] = useState(null)
  const [blackOpenNewImg, setBlackOpenNewImg] = useState(null)

  // Hover state with animation
  const [hoveredNodeLink, setHoveredNodeLink] = useState(null)
  const [animatedIconSizes, setAnimatedIconSizes] = useState({})
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })
  const animationRef = useRef()

  const [coloredNodes, setColoredNodes] = useState(nodes)

  useEffect(() => {
	// Apply colors based on current graph view
	const updatedNodes = nodes.map((node, index) => ({
	  ...node,
	  color: generateNodeColor(node, graphView, index),
	}))
	setColoredNodes(updatedNodes)
  }, [nodes, graphView])

  // Full screen ability
  const handleFullScreen = () => {
	if (!graphContainerRef.current) return

	const element = graphContainerRef.current

	if (element.requestFullscreen) {
	  element.requestFullscreen()
	} else if (element.webkitRequestFullscreen) {
	  element.webkitRequestFullscreen() // Safari
	} else if (element.msRequestFullscreen) {
	  element.msRequestFullscreen() // IE/Edge
	}
  }

  // Effects
  useEffect(() => {
	// Check if nodes are valid
	if (coloredNodes == null) return

	// Load imgs
	const imgWhite = new Image()
	imgWhite.crossOrigin = "anonymous"
	imgWhite.src = "/icons/openInNewWhite.svg"
	imgWhite.onload = () => setWhiteOpenNewImg(imgWhite)

	const imgBlack = new Image()
	imgBlack.crossOrigin = "anonymous"
	imgBlack.src = "/icons/openInNewBlack.svg"
	imgBlack.onload = () => setBlackOpenNewImg(imgBlack)
  }, [coloredNodes])

  // For mouse effect check
  const isMouseOverIcon = (node) => {
	if (!node?.__iconArea) return false

	const ia = node.__iconArea
	return mousePos.x >= ia.x && mousePos.x <= ia.x + ia.width && mousePos.y >= ia.y && mousePos.y <= ia.y + ia.height
  }

  // Animation loop for smooth transitions
  useEffect(() => {
	const animate = () => {
	  setAnimatedIconSizes((prev) => {
		const newSizes = { ...prev }
		let hasChanges = false

		coloredNodes.forEach((node) => {
		  const nodeId = node.id
		  const targetSize = hoveredNodeLink === node ? 31.2 : 24 // 24 * 1.3
		  const currentSize = prev[nodeId] || 24

		  // Smooth interpolation with easing
		  if (Math.abs(currentSize - targetSize) > 0.1) {
			const direction = currentSize < targetSize ? 1 : -1
			const distance = Math.abs(targetSize - currentSize)
			const easing = Math.min(distance * 0.3, 2) // Ease-in-out effect

			newSizes[nodeId] = currentSize + easing * direction
			hasChanges = true
		  } else if (currentSize !== targetSize) {
			newSizes[nodeId] = targetSize
			hasChanges = true
		  }
		})

		return hasChanges ? newSizes : prev
	  })

	  animationRef.current = requestAnimationFrame(animate)
	}

	animationRef.current = requestAnimationFrame(animate)

	return () => {
	  if (animationRef.current) {
		cancelAnimationFrame(animationRef.current)
	  }
	}
  }, [hoveredNodeLink, coloredNodes])

  // Return
  return (
	<div id="graph" ref={graphContainerRef}>
	  <ForceGraph
		ref={graphRef}
		graphData={{
		  nodes: coloredNodes,
		  links: links,
		}}
		enableNodeDrag={false}
		// Set up links
		linkWidth={4}
		linkColor={() => "rgba(200, 200, 200, 0.3)"}
		onEngineTick={() => {
		  if (graphRef.current) {
			// Set strength of links
			graphRef.current.d3Force("charge").strength(-100)
			graphRef.current.d3Force("link").distance(100)
		  }
		}}
		onNodeHover={(node, event) => {
		  if (event) {
			const graphCoords = graphRef.current.screen2GraphCoords(event.clientX, event.clientY)
			setMousePos(graphCoords)
		  }

		  // Only set as hovered node if mouse is over the icon area
		  setHoveredNodeLink(node && isMouseOverIcon(node) ? node : null)
		}}
		nodeCanvasObject={(node, ctx) => {
		  // Set up node
		  const label = node.site
		  const fontSize = 8
		  const baseIconSize = 12
		  const iconSize = animatedIconSizes[node.id] || baseIconSize
		  const iconSpacing = 4
		  const padding = fontSize * 0.8

		  ctx.font = `700 ${fontSize}px Montserrat, Sans-Serif`
		  const textWidth = ctx.measureText(label).width

		  const bckgWidth = textWidth + baseIconSize + padding * 2 + iconSpacing
		  const bckgHeight = fontSize + padding * 2
		  const bckgDimensions = [bckgWidth, bckgHeight]
		  node.__bckgDimensions = bckgDimensions

		  // Draw backdrop shadow
		  ctx.save()
		  ctx.shadowColor = "rgba(0, 0, 0, 0.2)"
		  ctx.shadowBlur = 15
		  ctx.shadowOffsetX = 0
		  ctx.shadowOffsetY = 4

		  // Draw background with shadow
		  ctx.fillStyle = node.color
		  const borderRadius = 4
		  ctx.beginPath()
		  ctx.roundRect(
			node.x - bckgDimensions[0] / 2,
			node.y - bckgDimensions[1] / 2,
			bckgDimensions[0],
			bckgDimensions[1],
			borderRadius,
		  )
		  ctx.fill()

		  ctx.restore() // Reset shadow for other elements

		  // Draw text
		  ctx.textAlign = "center"
		  ctx.textBaseline = "middle"
		  ctx.fillStyle = "rgb(0, 0, 0)"
		  ctx.fillText(label, node.x - (fontSize + iconSpacing + baseIconSize / 2) / 2, node.y)

		  // Draw img once loaded
		  if (blackOpenNewImg) {
			// Center the icon properly regardless of current animated size
			const iconX = node.x + bckgWidth / 2 - (iconSize - (iconSize - baseIconSize) / 2) - padding / 2
			const iconY = node.y - iconSize / 2

			ctx.drawImage(blackOpenNewImg, iconX, iconY, iconSize, iconSize)

			node.__iconArea = { x: iconX, y: iconY, width: iconSize, height: iconSize }
		  }
		}}
		nodePointerAreaPaint={(node, color, ctx) => {
		  ctx.fillStyle = color
		  const bckgDimensions = node.__bckgDimensions
		  bckgDimensions &&
			ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions)
		}}
		onNodeClick={(node, event) => {
		  if (!blackOpenNewImg || !whiteOpenNewImg) {
			return
		  }

		  const graphCoords = graphRef.current.screen2GraphCoords(event.clientX, event.clientY)
		  if (node.__iconArea) {
			const ia = node.__iconArea
			if (
			  graphCoords.x >= ia.x &&
			  graphCoords.x <= ia.x + ia.width &&
			  graphCoords.y >= ia.y &&
			  graphCoords.y <= ia.y + ia.height
			) {
			  event.preventDefault()
			  window.open(node.link, "_blank")
			  return
			}
		  }

		  console.log("Node clicked:", node)
		}}
	  />

	  <GraphToolbar handleFullScreen={handleFullScreen} />
	  <GraphOptions />
	</div>
  )
}

export default Graph
