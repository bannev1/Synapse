using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;

namespace api.Models.Graph
{
    public class Node
    {
        [Key]
        public int id { get; set; }

        [Required]
        public string Name { get; set; }
        [Required]
        public List<int> Colors { get; set; }
    }
}
