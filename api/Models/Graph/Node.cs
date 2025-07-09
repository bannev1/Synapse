using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;

namespace api.Models.Graph
{
    public enum NodeTypes
    {
        Source,
        Title,
        Topic
    }

    public class Node
    {
        [Key]
        public int id { get; set; }

        public string Name { get; set; }
        public List<int> Colors { get; set; }

        [Column(TypeName = "nvarchar(24)")]
        public NodeTypes NodeType { get; set; }

        public virtual List<Node> Neighbors { get; set; }
    }
}
