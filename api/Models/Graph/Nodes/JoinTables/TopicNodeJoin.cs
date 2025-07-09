using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using api.Models.Graph.Nodes;

namespace api.Models.Graph.Nodes.JoinTables
{
    public class TopicNodeJoin
    {
        [Key]
        public int id { get; set; }

        [ForeignKey(nameof(id))]
        public TopicNode topicNode { get; set; }


    }
}
