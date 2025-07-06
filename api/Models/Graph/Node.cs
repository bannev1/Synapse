using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;

namespace api.Models.Graph
{
    public class Node
    {
        [Key]
        public int id { get; set; }

        public string Name { get; set; }
        public int[] Colors { get; set; }
        public virtual List<Node> neighbors { get; set; }
    }
}
