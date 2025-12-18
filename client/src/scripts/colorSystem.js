// Automated color system for graph nodes
// Maps categories to colors based on the three graph views

const TOPICAL_COLORS = [
  "#FF6B6B", // Red
  "#4ECDC4", // Teal
  "#45B7D1", // Blue
  "#FFA07A", // Light Salmon
  "#98D8C8", // Mint
  "#F7DC6F", // Yellow
  "#BB8FCE", // Purple
  "#85C1E2", // Light Blue
]

const MEDIUM_COLORS = [
  "#3498DB", // Article (Blue)
  "#E74C3C", // Video (Red)
  "#27AE60", // Research Paper (Green)
  "#F39C12", // Blog (Orange)
  "#9B59B6", // Podcast (Purple)
  "#16A085", // News (Dark Teal)
]

const LOCATION_COLORS = [
  "#1ABC9C", // Asia
  "#3498DB", // Europe
  "#E74C3C", // Americas
  "#F39C12", // Africa
  "#9B59B6", // Oceania
]

export const getColorForCategory = (
  category,
  view,
  index,
) => {
  if (!category) {
    return "#95A5A6" // Gray for uncategorized
  }

  let colorArray
  let hashCode = 0

  // Generate consistent hash from category string
  for (let i = 0; i < category.length; i++) {
    const char = category.charCodeAt(i)
    hashCode = (hashCode << 5) - hashCode + char
    hashCode = hashCode & hashCode // Convert to 32bit integer
  }

  switch (view) {
    case "topical":
      colorArray = TOPICAL_COLORS
      break
    case "medium":
      colorArray = MEDIUM_COLORS
      break
    case "location":
      colorArray = LOCATION_COLORS
      break
    default:
      colorArray = TOPICAL_COLORS
  }

  const colorIndex = Math.abs(hashCode) % colorArray.length
  return colorArray[colorIndex]
}

export const getCategoryFromNode = (node, view) => {
  if (!node.category) return undefined

  switch (view) {
    case "topical":
      return node.category.topical
    case "medium":
      return node.category.medium
    case "location":
      return node.category.location
    default:
      return node.category.topical
  }
}

export const generateNodeColor = (node, view, index) => {
  const category = getCategoryFromNode(node, view)
  return getColorForCategory(category, view, index)
}
