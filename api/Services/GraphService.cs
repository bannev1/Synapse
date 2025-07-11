using api.Models.Graph;
using Microsoft.AspNetCore.StaticFiles;

namespace api.Services
{
    public static class GraphService
    {
        // CONSTRUCT
        // Construct topic type graph
        public static GraphNode? TopicalConstructor(string query)
        {
            return null;
        }

        // Construct media type graph
        public static GraphNode? MediumConstructor(string query)
        {
            return null;
        }

        // Construct location type graph
        public static GraphNode? LocationalConstructor(string query)
        {
            return null;
        }


        // COLOR
        // Color GraphNode Nodes with colors given
        public static GraphNode ColorGraph(GraphNode graph, List<List<int>> colors)
        {
            return graph;
        }


        // ADD NODE
        // Add node by source
        public static GraphNode AddNodeBySource(GraphNode graph, string source)
        {
            // Logic to add a node by source
            return graph;
        }

        // Add node by node
        public static GraphNode AddNodeByNode(GraphNode graph, GraphNode node)
        {
            // Logic to add a node by another node
            return graph;
        }


        // DELETE NODE
        // Delete node by source
        public static GraphNode DeleteNodeBySource(GraphNode graph, string source)
        {
            // Logic to delete a node by source
            return graph;
        }

        // Delete node by node
        public static GraphNode DeleteNodeByNode(GraphNode graph, GraphNode node)
        {
            // Logic to delete a node by another node
            return graph;
        }


        // LIST GRAPH
        public static List<NodeList> GetNodeList(GraphNode graph)
        {
            
        }


        // GET PATH OF NODE
        public static List<Node> GetPath(GraphNode graph, Node targetNode)
        {
            List<Node> path = new List<Node>();

            return path;
        }


        // CREATE COMPARE GRAPH
        public static GraphNode CreateCompareGraph(GraphNode graph1, GraphNode graph2)
        {
            // Logic to create a compare graph
            return new GraphNode();
        }
    }


    // Representation of nodes as a list
    public class NodeList
    {
        public Node NodeValue { get; set; }
        public string Value { get; set; }
        public List<NodeList>? InnerNodes { get; set; }
        

        public NodeList(Node node)
        {
            NodeValue = node;
            Value = node.Name;
        }

        public NodeList(Node node, string nodeValue)
        {
            NodeValue = node;
            Value = nodeValue;
        }
    }
}