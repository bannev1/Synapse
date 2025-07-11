using api.Models.Graph;
using System.ComponentModel.DataAnnotations;

namespace api.Models
{
    public class Cache
    {
        [Key]
        public int id { get; set; }

        [Required]
        public string Query { get; set; }
        [Required]
        public string GraphType { get; set; }

        [Required]
        public GraphNode Graph { get; set; }

        [Required]
        public DateTime Timestamp { get; set; }
    }
}
