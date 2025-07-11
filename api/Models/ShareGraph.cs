using System.ComponentModel.DataAnnotations;

using api.Models.Graph;

namespace api.Models
{
    public class ShareGraph
    {
        [Key]
        public string id { get; set; }

        [Required]
        public GraphNode Graph {  get; set; }
    }
}
