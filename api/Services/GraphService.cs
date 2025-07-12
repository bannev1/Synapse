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
        public static GraphNode? TopicalConstructor(string query, int depth, List<List<int>>? colors = null)
        {
            List<string>? topics = new List<string>();

            // Get topics
            try
            {
                topics = SearchService.GetTopics(query);

                if (topics == null)
                    return null;
            } catch (HttpRequestException)
            {
                return null;
            }

            TitleNode? titleNode = new TitleNode();

            titleNode.Name = query;
            titleNode.TopicNodes = new List<TopicNode>();

            // Create sources dictionary reference
            Dictionary<string, SourceNode> sources = new Dictionary<string, SourceNode>();

            // Populate TitleNode with topics
            foreach (string topic in topics)
            {
                if (topic == null)
                    continue;

                // Define current topic node
                TopicNode currTopic = new TopicNode();
                currTopic.Name = topic;
                currTopic.TitleNode = titleNode;
                currTopic.SourceNodes = new List<SourceTopicJoin>();

                // Populate with first level of sourcenodes
                string topicQuery = $"{query} {topic}";
                List<string> topicSources = SearchService.SearchQuery(topicQuery);

                // Create source nodes
                foreach (string source in topicSources)
                {
                    SourceTopicJoin joinSource = new SourceTopicJoin();
                    SourceNode currSource = new SourceNode();
                    currSource.Source = source;
                    currSource.TitleNode = titleNode;
                    currSource.TopicNodes = new List<SourceTopicJoin>();
                    currSource.Topics = new List<string>();
                    currSource.SourceNodes = new List<SourceNodeJoin>();

                    // Check if already exists in sources
                    if (sources.ContainsKey(source))
                        currSource = sources[source];
                    else
                    {
                        currSource = SearchService.SearchSourceInformation(currSource); // Populate source with information
                        currSource.Name = SearchService.GetSourceName(source);
                    }

                    // Add topics
                    currSource.Topics.Add(topic);

                    // Populate join table
                    joinSource.SourceNode = currSource;
                    joinSource.TopicNode = currTopic;
                    
                    // Add references
                    currSource.TopicNodes.Add(joinSource);
                    currTopic.SourceNodes.Add(joinSource);

                    // Add reference to sources
                    sources[source] = currSource;
                }

                titleNode.TopicNodes.Add(currTopic);
            }


            // Construct titleNode graph
            foreach (TopicNode topic in titleNode.TopicNodes)
            {
                foreach (SourceTopicJoin source in topic.SourceNodes)
                {
                    TopicalConstructor(titleNode, depth, source.SourceNode, query, sources, 1);
                }
            }

            if (titleNode == null)
                return null;

            // Construct graph from titleNode
            GraphNode? graph = new GraphNode();
            graph.TitleNode = titleNode;
            graph.Name = query;
            graph.Depth = depth;
            graph.Sources = sources.Keys.ToList();

            // Color graph if colors specified
            if (colors != null)
                graph = ColorGraph(graph, colors);

            return graph;
        }

        // Construct graph recursively
        private static void TopicalConstructor(TitleNode titleNode, int depth, SourceNode currNode, string query, Dictionary<string, SourceNode> sources, int currDepth)
        {
            if (currDepth >= depth)
                return;

            currDepth++;

            // Get references for each
            List<string> sourceReferences = SearchService.SearchReferences(currNode.Source);

            // Make sources
            foreach (string source in sourceReferences)
            {
                SourceNodeJoin neighborJoinParent = new SourceNodeJoin();
                SourceNodeJoin neighborJoinChild = new SourceNodeJoin();

                // Set defaults
                SourceNode currSource = new SourceNode();
                currSource.Source = source;
                currSource.TitleNode = titleNode;
                currSource.TopicNodes = new List<SourceTopicJoin>();
                currSource.Topics = new List<string>();
                currSource.SourceNodes = new List<SourceNodeJoin>();

                // Check if already exists in sources
                if (sources.ContainsKey(source))
                    currSource = sources[source];
                else
                {
                    currSource = SearchService.SearchSourceInformation(currSource); // Populate source with information
                    currSource.Name = SearchService.GetSourceName(source);
                }

                // Add topics
                foreach (string topic in currNode.Topics)
                {
                    if (!currSource.Topics.Contains(topic)) // If topic is not already in node then add (not adding actual reference just string)
                        currSource.Topics.Add(topic);
                }

                // Set relationships
                neighborJoinParent.SourceNode1 = currNode;
                neighborJoinParent.SourceNode2 = currSource;

                neighborJoinChild.SourceNode1 = currSource;
                neighborJoinChild.SourceNode2 = currNode;

                // Add relationships
                currNode.SourceNodes.Add(neighborJoinParent);
                currSource.SourceNodes.Add(neighborJoinChild);

                sources[source] = currSource;

                TopicalConstructor(titleNode, depth, currSource, query, sources, currDepth);
            }
        }

        // Construct media type graph
        public static GraphNode? MediumConstructor(string query, int depth, int initialSize = 15, List<List<int>>? colors = null)
        {
            // Add default sources which have the highest chance of being related to the prompt
            List<string> searchSources = SearchService.SearchQuery(query, amount: initialSize);

            // Define base title
            TitleNode titleNode = new TitleNode();
            titleNode.Name = query;
            titleNode.TopicNodes = new List<TopicNode>();

            // Create sources dictionary reference
            Dictionary<string, SourceNode> sources = new Dictionary<string, SourceNode>();

            // Create main mediums list
            Dictionary<string, TopicNode> mediums = new Dictionary<string, TopicNode>();

            foreach (string source in searchSources)
            {
                // Create current node
                SourceNode currNode = new SourceNode();
                currNode.Source = source;
                currNode.TitleNode = titleNode;
                currNode.TopicNodes = new List<SourceTopicJoin>();
                currNode.Topics = new List<string>(); // Won't populize
                currNode.SourceNodes = new List<SourceNodeJoin>();

                if (sources.Keys.Contains(source))
                    currNode = sources[source];
                else
                {
                    currNode = SearchService.SearchSourceInformation(currNode);
                    currNode.Name = SearchService.GetSourceName(source);
                }

                // Add mediums
                foreach (string medium in currNode.Mediums)
                {
                    // If medium not already there, then create
                    if (!mediums.Keys.Contains(medium))
                    {
                        TopicNode mediumTopic = new TopicNode();
                        mediumTopic.Name = medium;
                        mediumTopic.SourceNodes = new List<SourceTopicJoin>();
                        mediumTopic.TitleNode = titleNode;

                        mediums[medium] = mediumTopic;

                        titleNode.TopicNodes.Add(mediumTopic);
                    }

                    // Add relationship/references
                    SourceTopicJoin topicJoin = new SourceTopicJoin();
                    topicJoin.TopicNode = mediums[medium];
                    topicJoin.SourceNode = currNode;

                    currNode.TopicNodes.Add(topicJoin);
                    mediums[medium].SourceNodes.Add(topicJoin);
                }

                // Reference in sources
                sources[source] = currNode;

                // Create recursive links
                MediumConstructor(titleNode, depth, currNode, query, sources, mediums, 1);
            }

            // Construct graph from titleNode
            GraphNode? graph = new GraphNode();
            graph.TitleNode = titleNode;
            graph.Name = query;
            graph.Depth = depth;
            graph.Sources = sources.Keys.ToList();

            // Color graph if colors specified
            if (colors != null)
                graph = ColorGraph(graph, colors);

            return graph;
        }

        // Construct graph recursively
        private static void MediumConstructor(TitleNode titleNode, int depth, SourceNode currNode, string query, Dictionary<string, SourceNode> sources, Dictionary<string, TopicNode> mediums, int currDepth)
        {
            // Check if max depth reached
            if (currDepth >= depth)
                return;

            currDepth++;

            // Get references for each
            List<string> sourceReferences = SearchService.SearchReferences(currNode.Source);

            // Make sources
            foreach (string source in sourceReferences)
            {
                SourceNodeJoin neighborJoinParent = new SourceNodeJoin();
                SourceNodeJoin neighborJoinChild = new SourceNodeJoin();

                // Set defaults
                SourceNode currSource = new SourceNode();
                currSource.Source = source;
                currSource.TitleNode = titleNode;
                currSource.TopicNodes = new List<SourceTopicJoin>();
                currSource.Topics = new List<string>(); // Don't populate this
                currSource.SourceNodes = new List<SourceNodeJoin>();

                // Check if already exists in sources
                if (sources.ContainsKey(source))
                    currSource = sources[source];
                else
                {
                    currSource = SearchService.SearchSourceInformation(currSource); // Populate source with information
                    currSource.Name = SearchService.GetSourceName(source);
                }

                // Add topics
                foreach (string medium in currSource.Mediums)
                {
                    // If medium not already there, then create
                    if (!mediums.Keys.Contains(medium))
                    {
                        TopicNode mediumTopic = new TopicNode();
                        mediumTopic.Name = medium;
                        mediumTopic.SourceNodes = new List<SourceTopicJoin>();
                        mediumTopic.TitleNode = titleNode;

                        mediums[medium] = mediumTopic;

                        titleNode.TopicNodes.Add(mediumTopic);
                    }

                    // Add relationship/references
                    SourceTopicJoin topicJoin = new SourceTopicJoin();
                    topicJoin.TopicNode = mediums[medium];
                    topicJoin.SourceNode = currSource;

                    currSource.TopicNodes.Add(topicJoin);
                    mediums[medium].SourceNodes.Add(topicJoin);
                }

                // Set relationships
                neighborJoinParent.SourceNode1 = currNode;
                neighborJoinParent.SourceNode2 = currSource;

                neighborJoinChild.SourceNode1 = currSource;
                neighborJoinChild.SourceNode2 = currNode;

                // Add relationships
                currNode.SourceNodes.Add(neighborJoinParent);
                currSource.SourceNodes.Add(neighborJoinChild);

                sources[source] = currSource;

                MediumConstructor(titleNode, depth, currSource, query, sources, mediums, currDepth);
            }
        }

        // Construct location type graph
        public static GraphNode? LocationalConstructor(string query, int depth, int initialSize = 15, List<List<int>>? colors = null)
        {
            // Add default sources which have the highest chance of being related to the prompt
            List<string> searchSources = SearchService.SearchQuery(query, amount: initialSize);

            // Define base title
            TitleNode titleNode = new TitleNode();
            titleNode.Name = query;
            titleNode.TopicNodes = new List<TopicNode>();

            // Create sources dictionary reference
            Dictionary<string, SourceNode> sources = new Dictionary<string, SourceNode>();

            // Create main mediums list
            Dictionary<string, TopicNode> locations = new Dictionary<string, TopicNode>();

            foreach (string source in searchSources)
            {
                // Create current node
                SourceNode currNode = new SourceNode();
                currNode.Source = source;
                currNode.TitleNode = titleNode;
                currNode.TopicNodes = new List<SourceTopicJoin>();
                currNode.Topics = new List<string>(); // Won't populize
                currNode.SourceNodes = new List<SourceNodeJoin>();

                if (sources.Keys.Contains(source))
                    currNode = sources[source];
                else
                {
                    currNode = SearchService.SearchSourceInformation(currNode);
                    currNode.Name = SearchService.GetSourceName(source);
                }

                // Add locations
                string location = currNode.Location;

                // If location not already there, then create
                if (!locations.Keys.Contains(location))
                {
                    TopicNode mediumTopic = new TopicNode();
                    mediumTopic.Name = location;
                    mediumTopic.SourceNodes = new List<SourceTopicJoin>();
                    mediumTopic.TitleNode = titleNode;

                    locations[location] = mediumTopic;

                    titleNode.TopicNodes.Add(mediumTopic);
                }

                // Add relationship/references
                SourceTopicJoin topicJoin = new SourceTopicJoin();
                topicJoin.TopicNode = locations[location];
                topicJoin.SourceNode = currNode;

                currNode.TopicNodes.Add(topicJoin);
                locations[location].SourceNodes.Add(topicJoin);

                // Reference in sources
                sources[source] = currNode;

                // Create recursive links
                LocationalConstructor(titleNode, depth, currNode, query, sources, locations, 1);
            }

            // Construct graph from titleNode
            GraphNode? graph = new GraphNode();
            graph.TitleNode = titleNode;
            graph.Name = query;
            graph.Depth = depth;
            graph.Sources = sources.Keys.ToList();

            // Color graph if colors specified
            if (colors != null)
                graph = ColorGraph(graph, colors);

            return graph;
        }

        // Construct graph recursively
        private static void LocationalConstructor(TitleNode titleNode, int depth, SourceNode currNode, string query, Dictionary<string, SourceNode> sources, Dictionary<string, TopicNode> locations, int currDepth)
        {
            // Check if max depth reached
            if (currDepth >= depth)
                return;

            currDepth++;

            // Get references for each
            List<string> sourceReferences = SearchService.SearchReferences(currNode.Source);

            // Make sources
            foreach (string source in sourceReferences)
            {
                SourceNodeJoin neighborJoinParent = new SourceNodeJoin();
                SourceNodeJoin neighborJoinChild = new SourceNodeJoin();

                // Set defaults
                SourceNode currSource = new SourceNode();
                currSource.Source = source;
                currSource.TitleNode = titleNode;
                currSource.TopicNodes = new List<SourceTopicJoin>();
                currSource.Topics = new List<string>(); // Don't populate this
                currSource.SourceNodes = new List<SourceNodeJoin>();

                // Check if already exists in sources
                if (sources.ContainsKey(source))
                    currSource = sources[source];
                else
                {
                    currSource = SearchService.SearchSourceInformation(currSource); // Populate source with information
                    currSource.Name = SearchService.GetSourceName(source);
                }

                // Add topic
                string location = currSource.Location;
                if (!locations.Keys.Contains(location))
                {
                    TopicNode mediumTopic = new TopicNode();
                    mediumTopic.Name = location;
                    mediumTopic.SourceNodes = new List<SourceTopicJoin>();
                    mediumTopic.TitleNode = titleNode;

                    locations[location] = mediumTopic;

                    titleNode.TopicNodes.Add(mediumTopic);
                }

                // Add relationship/references
                SourceTopicJoin topicJoin = new SourceTopicJoin();
                topicJoin.TopicNode = locations[location];
                topicJoin.SourceNode = currSource;

                currSource.TopicNodes.Add(topicJoin);
                locations[location].SourceNodes.Add(topicJoin);

                // Set relationships
                neighborJoinParent.SourceNode1 = currNode;
                neighborJoinParent.SourceNode2 = currSource;

                neighborJoinChild.SourceNode1 = currSource;
                neighborJoinChild.SourceNode2 = currNode;

                // Add relationships
                currNode.SourceNodes.Add(neighborJoinParent);
                currSource.SourceNodes.Add(neighborJoinChild);

                sources[source] = currSource;

                MediumConstructor(titleNode, depth, currSource, query, sources, locations, currDepth);
            }
        }


        // COLOR
        // Color GraphNode Nodes with colors given
        public static GraphNode? ColorGraph(GraphNode graph, List<List<int>> colors)
        {
            // Access titleNode
            TitleNode titleNode = graph.TitleNode;

            Dictionary<SourceNode, List<List<int>>> ColorMaps = new Dictionary<SourceNode, List<List<int>>>();
            
            // Check colors and assign to each topic
            for (int index = 0; index < titleNode.TopicNodes.Count(); index++) 
            {
                if (index >= colors.Count()) // If not enough colors
                    return null;

                TopicNode currTopic = titleNode.TopicNodes[index];

                currTopic.Colors = colors[index]; // Assign colors

                foreach (SourceTopicJoin source in currTopic.SourceNodes)
                    ColorGraph(titleNode, source.SourceNode, ColorMaps);
            }

            // Blend colors
            foreach (SourceNode currNode in ColorMaps.Keys)
            {
                List<List<int>> colorNode = new List<List<int>>();

                // Add weighting
                foreach (List<int> colorSet in ColorMaps[currNode])
                {
                    colorSet.Add((int)((1 / (colorNode.Count())) * 100)); // Add weighting %

                    colorNode.Add(colorSet);
                }

                // Use color blender
                List<int> blendedColor = ColorBlender(colorNode);

                // Assign colors in node
                currNode.Colors = blendedColor;
            }

            return graph;
        }

        // Color graph recursively
        private static void ColorGraph(TitleNode titleNode, SourceNode currNode, Dictionary<SourceNode, List<List<int>>> colorMap, bool recurse = true)
        {
            List<List<int>> nodeColors = new List<List<int>>(); // Each inner list has 3 values – [R, G, B, weight (as a %)]

            // Iterate through topic nodes – highest weighting
            if (currNode.TopicNodes.Count() > 0)
            {
                int topicPercent = 90; // Percent topic nodes should color currNode

                foreach (SourceTopicJoin topicJoin in currNode.TopicNodes)
                {
                    TopicNode currTopic = topicJoin.TopicNode;

                    // Make sure not null
                    if (currTopic.Colors == null)
                        continue;

                    List<int> topicColors = new List<int>();

                    // Add fade
                    foreach (int color in currTopic.Colors)
                    {
                        topicColors.Add((int)(color * (topicPercent / 100))); // Fade color
                    }
                }

                // Add fade
                List<int> fade = new List<int>() { 0, 0, 0, (100-topicPercent) };

                nodeColors.Add(fade);
            }
            // Iterate through neighboring nodes – IF not directly under topic node
            else {
                // Check if colors already exist for node
                if (colorMap.Keys.Contains(currNode))
                    nodeColors = colorMap[currNode];

                // Go through each neighbor
                foreach (SourceNodeJoin neighboringJoin in currNode.SourceNodes)
                {
                    SourceNode neighborNode = neighboringJoin.SourceNode2;

                    // Check if has colors
                    if (colorMap.Keys.Contains(neighborNode))
                    {
                        nodeColors.AddRange(colorMap[neighborNode]);
                    } else
                    {
                        if (neighborNode.TopicNodes.Count() > 0)
                        {
                            ColorGraph(titleNode, neighborNode, colorMap, false); // Get neighbor node to get color

                            // Add new neighbor color
                            if (colorMap.Keys.Contains(neighborNode))
                            {
                                nodeColors.AddRange(colorMap[neighborNode]);
                            }
                        }
                    }
                }

                // Make sure all neighbors have connected colors
                foreach (List<int> ColorSet in nodeColors) 
                { 
                    foreach (SourceNodeJoin neighboringJoin in currNode.SourceNodes)
                    {
                        SourceNode neighborNode = neighboringJoin.SourceNode2;

                        if (neighborNode.TopicNodes.Count() == 0)
                        {
                            if (colorMap.Keys.Contains(neighborNode))
                            {
                                // If neighbor doesn't have current color and isn't directly topic node
                                if (!colorMap[neighborNode].Contains(ColorSet))
                                    colorMap[neighborNode].Add(ColorSet);
                            }
                        }
                    }   
                }
            }

            // Add colors
            colorMap[currNode] = nodeColors;

            // Go through neighbors
            if (recurse)
                foreach (SourceNodeJoin neighboringJoin in currNode.SourceNodes)
                {
                    if (neighboringJoin.SourceNode2.Colors == null) // Make sure not yet colored
                        ColorGraph(titleNode, neighboringJoin.SourceNode2, colorMap);
                }
        }

        // Color blender given a list of [R, G, B, weight (%)]
        private static List<int> ColorBlender(List<List<int>> colors)
        {
            if (colors == null || colors.Count == 0)
                return new List<int> { 128, 128, 128 }; // Default gray

            int totalR = 0, totalG = 0, totalB = 0;
            int totalWeight = 0;

            foreach (var color in colors)
            {
                if (color.Count < 4) continue; // Skip invalid entries

                int weight = color[3];
                totalR += color[0] * weight;
                totalG += color[1] * weight;
                totalB += color[2] * weight;
                totalWeight += weight;
            }

            if (totalWeight == 0)
                return new List<int> { 128, 128, 128 }; // Fallback gray

            return new List<int>
            {
                totalR / totalWeight,
                totalG / totalWeight,
                totalB / totalWeight
            };
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