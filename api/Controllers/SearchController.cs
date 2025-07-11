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
    }
}