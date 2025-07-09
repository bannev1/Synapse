using api.Models.Graph;
using Microsoft.AspNetCore.Mvc;

namespace api.Controllers
{
    [Route("/")]
    [ApiController]
    public class SearchController : Controller
    {
        [HttpGet("/construct/{query}")]
        public IActionResult construct(string query, int depth, List<string> sources, string graphType, List<List<int>> colors)
        {
            // Make sure correct graph type
            if (graphType != "topical" || graphType != "medium" || graphType != "location")
            {
                return BadRequest();
            }

            GraphNode graph = new GraphNode();

            return Ok(graph);
        }
    }
}
