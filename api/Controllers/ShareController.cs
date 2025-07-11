using Microsoft.AspNetCore.Mvc;

using api.Models;
using api.Models.Graph;
using api.Models.Graph.Nodes;

using api.Data;

namespace api.Controllers
{
    [Route("/share")]
    [ApiController]
    public class ShareController : Controller
    {
        private readonly DataContext _dataContext;

        public ShareController(DataContext dataContext) 
        {
            _dataContext = dataContext;
        }

        // Make share URL for graph
        [HttpPost]
        public IActionResult share(GraphNode graph)
        {
            // Make new ShareGraph record
            ShareGraph shareGraph = new ShareGraph();
            shareGraph.Graph = graph;

            // Generate unique ID
            string id;
            do
            {
                id = Guid.NewGuid().ToString();
            } while (idExists(id));

            shareGraph.id = id;

            // Add to database
            _dataContext.ShareGraphs.Add(shareGraph);
            _dataContext.SaveChanges();


            return Ok();
        }

        [HttpGet("{id}")]
        public IActionResult get(string id)
        {
            // Check if ID exists
            if (!idExists(id))
            {
                return NotFound();
            }

            // Get the ShareGraph by ID
            ShareGraph shareGraph = _dataContext.ShareGraphs.FirstOrDefault(sg => sg.id == id);
            
            if (shareGraph == null) // Make sure not null
                return NotFound();


            return Ok(shareGraph.Graph);
        }

        [HttpPost("/save/{id}")]
        public IActionResult save(string id, GraphNode graph)
        {
            // Check if ID exists
            if (!idExists(id))
            {
                return NotFound();
            }

            // Get the ShareGraph by ID
            ShareGraph shareGraph = _dataContext.ShareGraphs.FirstOrDefault(sg => sg.id == id);

            if (shareGraph == null) // Make sure not null
                return NotFound();

            // Update graph
            shareGraph.Graph = graph;

            // Save changes to database
            _dataContext.SaveChanges();


            return Ok();
        }

        // Check if ID exists
        private bool idExists(string id)
        {
            return _dataContext.ShareGraphs.Any(sg => sg.id == id);
        }
    }
}
