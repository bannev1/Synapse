using api.Models.Graph;
using api.Models.Graph.Nodes.Relationships;
using System.ComponentModel.DataAnnotations;

namespace api.Models.Graph.Nodes
{
    public class TopicNode : Node 
    {
        [Required]
        public TitleNode TitleNode { get; set; }

        public virtual List<SourceTopicJoin> SourceNodes { get; set; }
    }
}