using api.Models.Graph.Nodes;
using System.ComponentModel.DataAnnotations;

namespace api.Models.Graph.Nodes.Relationships
{
    public class SourceNodeJoin
    {
        [Key]
        public int id { get; set; }

        [Required]
        public SourceNode SourceNode1 { get; set; }
        [Required]
        public SourceNode SourceNode2 { get; set; }
    }
}
