using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using api.Models.Graph;

namespace api.Models.Graph.Nodes
{
    public class SourceNode : Node
    {
        [Required]
        public string Source { get; set; }
        [Required]
        public virtual List<string> Topics { get; set; }
        [Required]
        public virtual List<string> Mediums { get; set; }
        [Required]
        public string Location { get; set; }

        [Required]
        public TitleNode TitleNode { get; set; }

        public List<SourceNode> SourceNodes { get; set; }
    }
}
