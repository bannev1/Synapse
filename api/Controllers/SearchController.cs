using Microsoft.AspNetCore.Mvc;

using api.Data;
using api.Models.Graph;
using api.Services;
using api.Models.Graph.Nodes;

namespace api.Controllers
{
    [Route("/")]
    [ApiController]
    public class SearchController : Controller
    {
        private readonly DataContext _dataContext;
        private readonly CacheController _cacheController;

        public readonly List<List<int>> DefaultColors;

        public SearchController(DataContext dataContext)
        {
            _dataContext = dataContext;

            // Initialize CacheController with DataContext
            _cacheController = new CacheController(dataContext);

            // Initialize DefaultColors
            DefaultColors = new List<List<int>>();
            DefaultColors.Add(new List<int>{ 255, 0, 0 });
        }

        [HttpGet("construct/{query}")]
        public IActionResult construct(string query, int depth, List<string> sources, string graphType, List<List<int>>? colors)
        {
            // Convert back to base format
            query = Uri.UnescapeDataString(query);

            // Check if query is in cache
            GraphNode? cachedGraph = _cacheController.GetCachedGraph(query, graphType);

            // If cached graph found, return it
            if (cachedGraph != null)
                return Ok(cachedGraph);

            GraphNode? graph;

            // Different graph types
            switch (graphType)
            {
                case "topical":
                    graph = GraphService.TopicalConstructor(query, depth, colors);
                    break;
                case "medium":
                    graph = GraphService.MediumConstructor(query, depth, colors: colors);
                    break;
                case "location":
                    graph = GraphService.LocationalConstructor(query, depth, colors: colors);
                    break;
                default:
                    return BadRequest("Invalid graph type");
            }

            // If error/graph not properly constructed
            if (graph == null)
            {
                return NotFound("Graph could not be constructed");
            }

            return Ok(graph);
        }

        [HttpGet("color")]
        public IActionResult colorGraph([FromBody] GraphNode graph, [FromBody] List<List<int>> colors)
        {
            // Color the graph
            GraphNode? coloredGraph = GraphService.ColorGraph(graph, colors);

            // Check if failure
            if (coloredGraph == null)
                return BadRequest("Failure to color");

            // Return the colored graph
            return Ok(coloredGraph);
        }

        [HttpGet("list")]
        public IActionResult listGraph([FromBody] GraphNode graph)
        {
            NodeList nodeList = GraphService.GetNodeList(graph);

            return Ok(nodeList);
        }

        [HttpGet("nodeAdd")]
        public IActionResult addNode([FromBody] GraphNode graph, [FromBody] string? source, [FromBody] SourceNode? node, [FromBody] List<Node> linkedNodes)
        {
            // Make sure correct parameters are provided
            if (source == null && node == null)
                return BadRequest("Either source or node must be provided");

            // Add node by source
            if (source != null)
                graph = GraphService.AddNodeBySource(graph, source, linkedNodes);

            // Add node by node
            if (node != null)
                graph = GraphService.AddNodeByNode(graph, node, linkedNodes);

            if (graph == null)
                return BadRequest("Failure to add node");

            return Ok(graph);
        }

        [HttpGet("nodeDelete")]
        public IActionResult deleteNode([FromBody] GraphNode graph, [FromBody] string? source, [FromBody] SourceNode? node)
        {
            // Make sure correct parameters are provided
            if (source == null && node == null)
                return BadRequest("Either source or node must be provided");

            // Delete node by source
            if (source != null)
                graph = GraphService.DeleteNodeBySource(graph, source);

            // Delete node by node
            if (node != null)
                graph = GraphService.DeleteNodeByNode(graph, node);

            return Ok(graph);
        }

        [HttpGet("nodePath")]
        public IActionResult getNodePath([FromBody] GraphNode graph, [FromBody] Node startingNode)
        {
            // Get the path of the node by source
            List<Node>? path = GraphService.GetPath(graph, startingNode);

            // If path is null, return not found
            if (path == null)
                return NotFound("Node not found");

            return Ok(path);
        }

        [HttpGet("compare")]
        public IActionResult compareGraphs([FromBody] GraphNode graph1, [FromBody] GraphNode graph2)
        {
            // Create a compare graph
            GraphNode? compareGraph = GraphService.CreateCompareGraph(graph1, graph2);

            if (compareGraph == null)
                return BadRequest("Failure to compare graphs");

            return Ok(compareGraph);
        }
    }
}