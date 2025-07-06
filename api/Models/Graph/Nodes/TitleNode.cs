using System.Collections.Generic;

namespace api.Models.Graph.Nodes
{
    public class TitleNode
    {
        public virtual List<TopicNode> Topics { get; set; }
    }
}
