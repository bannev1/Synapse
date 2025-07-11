using api.Models.Graph;
using System.ComponentModel.DataAnnotations;

namespace api.Models.Graph.Nodes
{
    public class TopicNode : Node 
    {
        [Required]
        public TitleNode TitleNode { get; set; }

        public virtual List<SourceNode> SourceNodes { get; set; }
    }
}