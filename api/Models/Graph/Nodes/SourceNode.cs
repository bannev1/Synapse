using System.Collections.Generic;
using api.Models.Graph;

namespace api.Models.Graph.Nodes
{
    public class SourceNode : Node
    {
        public string Source { get; set; }
        public virtual List<TopicNode> TopicNodes { get; set; }
        public virtual List<string> Topics { get; set; }
        public virtual List<string> Mediums { get; set; }
        public string Location { get; set; }
    }
}
