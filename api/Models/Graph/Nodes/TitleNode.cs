using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace api.Models.Graph.Nodes
{
    public class TitleNode : Node
    {
        [Required]
        public GraphNode GraphNode { get; set; }
    }
}
