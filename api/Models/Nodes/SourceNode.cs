using System.Collections.Generic;

using api.Models;
using api.Models.Nodes;

namespace api.Models.Nodes
{
    public class SourceNode : Node
    {
        public string Source { get; set; }
        public List<TopicNode> TopicNodes { get; set; }
        public List<string> Topics { get; set; }
        public List<string> Mediums { get; set; }
        public string Location { get; set; }
    }
}
