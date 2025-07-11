using api.Models.Graph.Nodes;
using System.ComponentModel.DataAnnotations;

namespace api.Models.Graph.Nodes.Relationships
{
    public class SourceTopicJoin
    {
        [Key]
        public int id { get; set; }

        [Required]
        public SourceNode SourceNode { get; set; }
        [Required]
        public TopicNode TopicNode { get; set; }
    }
}
