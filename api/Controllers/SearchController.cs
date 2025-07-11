using Microsoft.AspNetCore.Mvc;

using api.Data;
using api.Models.Graph;
using api.Services;

namespace api.Controllers
{
    [Route("/")]
    [ApiController]
    public class SearchController : Controller
    {
        private readonly DataContext _dataContext;

        public SearchController(DataContext dataContext)
        {
            _dataContext = dataContext;
        }

        [HttpGet("construct/{query}")]
        public IActionResult construct(string query, int depth, List<string> sources, string graphType, List<List<int>> colors)
        {
            // Convert back to base format
            query = Uri.UnescapeDataString(query);

            GraphNode? graph;

            // Different graph types
            switch (graphType)
            {
                case "topical":
                    graph = GraphService.TopicalConstructor(query);
                    break;
                case "medium":
                    graph = GraphService.MediumConstructor(query);
                    break;
                case "location":
                    graph = GraphService.LocationalConstructor(query);
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
            GraphNode coloredGraph = GraphService.ColorGraph(graph, colors);

            // Return the colored graph
            return Ok(coloredGraph);
        }

        [HttpGet("list")]
        public IActionResult listGraph([FromBody] GraphNode graph)
        {
            List<NodeList> nodeList = GraphService.GetNodeList(graph);

            return Ok(nodeList);
        }

        [HttpGet("nodeAdd")]
        public IActionResult addNode([FromBody] GraphNode graph, [FromBody] string? source, [FromBody] GraphNode? node)
        {
            // Make sure correct parameters are provided
            if (source == null && node == null)
                return BadRequest("Either source or node must be provided");

            // Add node by source
            if (source != null)
                graph = GraphService.AddNodeBySource(graph, source);

            // Add node by node
            if (node != null)
                graph = GraphService.AddNodeByNode(graph, node);

            return Ok(graph);
        }

        [HttpGet("nodeDelete")]
        public IActionResult deleteNode([FromBody] GraphNode graph, [FromBody] string? source, [FromBody] GraphNode? node)
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
            GraphNode compareGraph = GraphService.CreateCompareGraph(graph1, graph2);

            return Ok(compareGraph);
        }
    }
}