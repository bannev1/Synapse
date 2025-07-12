using Microsoft.AspNetCore.StaticFiles;

using api.Models.Graph;
using api.Models.Graph.Nodes;
using api.Models.Graph.Nodes.Relationships;

namespace api.Services
{
    public static class GraphService
    {
        // CONSTRUCT
        // Construct topic type graph
        public static GraphNode? TopicalConstructor(string query)
        {
            // Get topics
            List<string> topics = SearchService.GetTopics(query);
            return null;
        }

        public static GraphNode? TopicalConstructor(TitleNode titleNode, )

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
        public static NodeList GetNodeList(GraphNode graph, int depth = 5, Node? currNode = null, NodeList? currList = null, int currDepth = 0)
        {
            // Initialize
            if (currNode == null) // If node not specified
                currNode = graph.TitleNode;

            NodeList nodeList = new NodeList(currNode); // initialize current nodelist

            if (currList == null) // If not currList yet
                currList = nodeList;

            if (depth <= currDepth) // If max depth reached
                return nodeList;

            currDepth++; // Increase Depth

            Type nodeType = currNode.GetType();

            // If on TitleNode
            if (nodeType == typeof(TitleNode))
            {
                // Go through each topic
                foreach (TopicNode topic in ((TitleNode)currNode).TopicNodes)
                {
                    NodeList? result = GetNodeList(graph, depth, topic, currList, currDepth);

                    if (result != null)
                        currList.InnerNodes.Add(result); // Add to currList
                }
            } 
            // If on TopicNode
            else if (nodeType == typeof(TopicNode)) {
                foreach (SourceTopicJoin nodeJoin in ((TopicNode)currNode).SourceNodes)
                {
                    NodeList? result = GetNodeList(graph, depth, nodeJoin.SourceNode, currList, currDepth);

                    if (result != null)
                        currList.InnerNodes.Add(result);
                }
            } 
            // If on SourceNode
            else if (nodeType == typeof(SourceNode))
            {
                foreach (SourceNodeJoin nodeJoin in ((SourceNode)currNode).SourceNodes)
                {
                    NodeList? result = GetNodeList(graph, depth, nodeJoin.SourceNode2, currList, currDepth);

                    if (result != null)
                        currList.InnerNodes.Add(result);
                }
            }

            // Return list after having added all
            return currList;
        }


        // GET PATH OF NODE
        public static List<Node>? GetPath(GraphNode graph, Node targetNode, List<Node>? path = null, Node? currNode = null)
        {
            if (path == null)
                path = new List<Node>();

            if (currNode == null)
                currNode = graph.TitleNode;

            path.Add(currNode);

            if (targetNode == currNode)
                return path;

            Type nodeType = currNode.GetType();

            List<Node>? min = null;

            // If on TitleNode
            if (nodeType == typeof(TitleNode))
            {

                // Go through each topic
                foreach (TopicNode topic in ((TitleNode)currNode).TopicNodes)
                {
                    List<Node>? result = GetPath(graph, targetNode, path, topic);

                    if (result != null) 
                    {
                        if (min == null)
                            min = result;
                        else if (min.Count() > result.Count()) // Check which path is shorter
                            min = result;
                    }
                }
            }
            // If on TopicNode
            else if (nodeType == typeof(TopicNode))
            {
                foreach (SourceTopicJoin nodeJoin in ((TopicNode)currNode).SourceNodes)
                {
                    List<Node>? result = GetPath(graph, targetNode, path, nodeJoin.SourceNode);

                    if (result != null)
                    {
                        if (min == null)
                            min = result;
                        else if (min.Count() > result.Count())
                            min = result;
                    }
                }
            }
            // If on SourceNode
            else if (nodeType == typeof(SourceNode))
            {
                foreach (SourceNodeJoin nodeJoin in ((SourceNode)currNode).SourceNodes)
                {
                    List<Node>? result = GetPath(graph, targetNode, path, nodeJoin.SourceNode2);

                    if (result != null)
                    {
                        if (min == null)
                            min = result;
                        else if (min.Count() > result.Count())
                            min = result;
                    }
                }
            }

            // null meaning haven't returned path, thus not found targetNode through this path
            return min;
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
        public List<NodeList> InnerNodes = new List<NodeList>();
        

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

        public NodeList(NodeList nodeList)
        {
            NodeValue = nodeList.NodeValue;
            Value = nodeList.Value;
            InnerNodes = nodeList.InnerNodes ?? new List<NodeList>();
        }
    }
}