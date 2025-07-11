using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;

using api.Models.Graph.Nodes;

namespace api.Models.Graph
{
    public class GraphNode
    {
        [Key]
        public int id { get; set; }

        [Required]
        public string Name { get; set; }
        [Required]
        public int Depth { get; set; }
        [Required]
        public virtual List<string> Sources { get; set; }

        [Required]
        public TitleNode TitleNode { get; set; }
    }
}
