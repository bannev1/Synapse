using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;

using api.Models;
using api.Models.Nodes;

namespace api.Models
{
    public class GraphNode
    {
        [Key]
        public int id { get; set; }

        public string Name { get; set; }
        public Dictionary<TopicNode, Node> TopicNodes { get; set; }
        public int Depth { get; set; }
        public List<string> Sources { get; set; }
    }
}
