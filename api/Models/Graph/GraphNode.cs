using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;

using api.Models.Graph.Nodes;

namespace api.Models.Graph
{
    public class GraphNode
    {
        [Key]
        public int id { get; set; }

        public string Name { get; set; }
        public Dictionary<TopicNode, Node> TopicNodes { get; set; }
        public int Depth { get; set; }
        public virtual List<string> Sources { get; set; }
    }
}
