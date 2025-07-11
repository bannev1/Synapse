using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace api.Models.Graph.Nodes
{
    public class TitleNode : Node
    {
        [Required]
        public GraphNode GraphNode { get; set; }

        public virtual List<TopicNode> TopicNodes { get; set; }
    }
}
