using System.ComponentModel.DataAnnotations;

using api.Models.Graph;

namespace api.Models
{
    public class ShareGraph
    {
        [Key]
        public string id { get; set; }

        public string Name { get; set; }
        public GraphNode Graph {  get; set; }
    }
}
