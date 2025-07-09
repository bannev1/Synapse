using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace api.Models.Graph.Nodes
{
    public class TitleNode : Node
    {
        [Required]
        public virtual List<TopicNode> Topics { get; set; }

        public new NodeTypes NodeType = NodeTypes.Title;
    }
}
