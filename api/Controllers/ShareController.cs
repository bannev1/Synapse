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
        public ActionResult share()
        {
            return Ok();
        }
    }
}
