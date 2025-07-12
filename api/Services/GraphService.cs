using Microsoft.AspNetCore.StaticFiles;

using api.Models.Graph;
using api.Models.Graph.Nodes;
using api.Models.Graph.Nodes.Relationships;
using System.Xml.Linq;

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
            graph.Type = "topic";

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
            graph.Type = "medium";

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
            graph.Type = "location";

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

            // Create a dictionary to store color contributions for each node
            Dictionary<SourceNode, List<List<int>>> colorMaps = new Dictionary<SourceNode, List<List<int>>>();

            // Check colors and assign to each topic
            for (int index = 0; index < titleNode.TopicNodes.Count; index++)
            {
                // Validate color availability
                if (index >= colors.Count)
                    return null;

                TopicNode currTopic = titleNode.TopicNodes[index];
                currTopic.Colors = colors[index]; // Assign colors

                // Process each source node under this topic
                foreach (SourceTopicJoin source in currTopic.SourceNodes)
                {
                    ColorNode(titleNode, source.SourceNode, colorMaps, new HashSet<SourceNode>());
                }
            }

            // Blend colors for all collected nodes
            foreach (SourceNode currNode in colorMaps.Keys)
            {
                List<List<int>> colorContributions = colorMaps[currNode];

                // Only blend if we have valid contributions
                if (colorContributions.Count > 0)
                {
                    // Apply proper weighting
                    List<List<int>> weightedColors = new List<List<int>>();
                    int weightPerContribution = 100 / colorContributions.Count;

                    foreach (List<int> colorSet in colorContributions)
                    {
                        // Create a copy to avoid modifying original
                        List<int> weightedSet = new List<int>(colorSet);
                        weightedSet.Add(weightPerContribution);
                        weightedColors.Add(weightedSet);
                    }

                    currNode.Colors = ColorBlender(weightedColors);
                }
                else
                {
                    // Fallback to default color
                    currNode.Colors = new List<int> { 128, 128, 128 };
                }
            }

            return graph;
        }

        // Helper method to color individual nodes
        private static void ColorNode(TitleNode titleNode, SourceNode currNode, Dictionary<SourceNode, List<List<int>>> colorMap, HashSet<SourceNode> visited)
        {
            // Avoid cycles and re-processing
            if (visited.Contains(currNode)) return;
            visited.Add(currNode);

            List<List<int>> colorContributions = new List<List<int>>();
            bool hasDirectTopics = false;

            // Process direct topic connections first (highest priority)
            if (currNode.TopicNodes != null && currNode.TopicNodes.Count > 0)
            {
                hasDirectTopics = true;
                int topicPercent = 90; // Primary weight for topics

                foreach (SourceTopicJoin topicJoin in currNode.TopicNodes)
                {
                    TopicNode topic = topicJoin.TopicNode;

                    if (topic?.Colors != null)
                    {
                        // Create a weighted color contribution
                        List<int> weightedColor = new List<int>();
                        foreach (int component in topic.Colors)
                        {
                            // Apply topic percentage
                            weightedColor.Add((int)(component * (topicPercent / 100.0)));
                        }
                        // Add the weight for this contribution
                        weightedColor.Add(topicPercent / currNode.TopicNodes.Count);
                        colorContributions.Add(weightedColor);
                    }
                }
            }

            // Process neighbor contributions (secondary)
            if (!hasDirectTopics && currNode.SourceNodes != null && currNode.SourceNodes.Count > 0)
            {
                int validNeighbors = 0;

                foreach (SourceNodeJoin neighborJoin in currNode.SourceNodes)
                {
                    SourceNode neighbor = neighborJoin.SourceNode2;

                    if (neighbor == null) continue;

                    // Ensure neighbor is processed first
                    if (!colorMap.ContainsKey(neighbor))
                    {
                        ColorNode(titleNode, neighbor, colorMap, visited);
                    }

                    if (colorMap.ContainsKey(neighbor) && neighbor.Colors != null)
                    {
                        validNeighbors++;
                        // Create a copy of neighbor's color
                        List<int> neighborColor = new List<int>(neighbor.Colors);
                        colorContributions.Add(neighborColor);
                    }
                }

                // Add weights to neighbor contributions
                if (validNeighbors > 0)
                {
                    int weightPerNeighbor = 100 / validNeighbors;
                    foreach (List<int> contribution in colorContributions)
                    {
                        contribution.Add(weightPerNeighbor);
                    }
                }
            }

            // Register contributions for this node
            colorMap[currNode] = colorContributions;
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
                    Math.Clamp(totalR / totalWeight, 0, 255),
                    Math.Clamp(totalG / totalWeight, 0, 255),
                    Math.Clamp(totalB / totalWeight, 0, 255)
                };
        }


        // ADD NODE
        // Add node by source
        public static GraphNode? AddNodeBySource(GraphNode graph, string source, List<List<int>>? colors = null, bool addReferences = false, int referenceDepth = 3)
        {
            // Node Creation
            if (graph.Sources.Contains(source)) // If graph already has source
                return graph;

            graph.Sources.Add(source);

            // Set up title node
            TitleNode titleNode = graph.TitleNode;

            // Initialize node
            SourceNode node = new SourceNode();
            node.Source = source;
            node.TitleNode = titleNode;
            node.SourceNodes = new List<SourceNodeJoin>();
            node.TopicNodes = new List<SourceTopicJoin>();

            node = SearchService.SearchSourceInformation(node);
            node.Name = SearchService.GetSourceName(source);

            // Fetch references (if specified)
            List<string>? references = null;

            if (addReferences)
                references = SearchService.SearchReferences(source);

            switch (graph.Type)
            {
                // If graph is topical
                case "topic":

                    break;

                // If graph is medium based
                case "medium":
                    // Assign to corresponding topics
                    foreach (string medium in node.Mediums)
                    {
                        bool assigned = false;

                        foreach (TopicNode topic in titleNode.TopicNodes)
                        {
                            if (topic.Name == medium)
                            {
                                // Add relationship
                                SourceTopicJoin topicJoin = new SourceTopicJoin();
                                topicJoin.TopicNode = topic;
                                topicJoin.SourceNode = node;

                                topic.SourceNodes.Add(topicJoin);
                                node.TopicNodes.Add(topicJoin);

                                assigned = true;

                                break;
                            }
                        }

                        // If haven't found corresponding topic, then make new
                        if (!assigned)
                        {
                            // Create topic
                            TopicNode topic = new TopicNode();
                            topic.Name = medium;
                            topic.TitleNode = titleNode;
                            topic.SourceNodes = new List<SourceTopicJoin>();

                            // Create relationship
                            SourceTopicJoin topicJoin = new SourceTopicJoin();
                            topicJoin.TopicNode = topic;
                            topicJoin.SourceNode = node;

                            topic.SourceNodes.Add(topicJoin);
                            node.TopicNodes.Add(topicJoin);
                        }
                    }

                    // Add references (if specified)
                    if (addReferences)
                        AddReferenceMedium(graph, node, referenceDepth, 0);

                    break;

                // If graph is location based
                case "location":
                    // Assign to corresponding topics
                    bool assigned = false;

                    foreach (TopicNode topic in titleNode.TopicNodes)
                    {
                        if (topic.Name == node.Location)
                        {
                            // Add relationship
                            SourceTopicJoin topicJoin = new SourceTopicJoin();
                            topicJoin.TopicNode = topic;
                            topicJoin.SourceNode = node;

                            topic.SourceNodes.Add(topicJoin);
                            node.TopicNodes.Add(topicJoin);

                            assigned = true;

                            break;
                        }
                    }

                    // If haven't found corresponding topic, then make new
                    if (!assigned)
                    {
                        // Create topic
                        TopicNode topic = new TopicNode();
                        topic.Name = node.Location;
                        topic.TitleNode = titleNode;
                        topic.SourceNodes = new List<SourceTopicJoin>();

                        // Create relationship
                        SourceTopicJoin topicJoin = new SourceTopicJoin();
                        topicJoin.TopicNode = topic;
                        topicJoin.SourceNode = node;

                        topic.SourceNodes.Add(topicJoin);
                        node.TopicNodes.Add(topicJoin);
                    }

                    // Add references (if specified)
                    if (addReferences)
                        AddReferenceLocation(graph, node, referenceDepth, 0);

                    break;

                // Else error
                default:
                    return null;
            }

            // Re-color graph (if colors specified)
            if (colors != null)
                ColorGraph(graph, colors);

            return graph;
        }

        private static void AddReferenceMedium(GraphNode graph, SourceNode currNode, int depth, int currDepth)
        {
            // Make sure not at max depth yet
            if (currDepth >= depth)
                return;

            currDepth++;

            List<string> references = SearchService.SearchReferences(currNode.Source);

            // Get all neighbors
            foreach (string source in references)
            {
                // Add relationship basis
                SourceNodeJoin nodeJoinParent = new SourceNodeJoin();
                SourceNodeJoin nodeJoinChild = new SourceNodeJoin();

                nodeJoinParent.SourceNode1 = currNode;
                nodeJoinChild.SourceNode2 = currNode;

                SourceNode neighborNode;

                // Check if source already exists
                if (graph.Sources.Contains(source))
                {
                    List<Node> path = GetPathBySource(graph, source);

                    neighborNode = (SourceNode)path[path.Count - 1]; // Get last element of path (found node)
                } else
                {
                    // Create new node
                    neighborNode = new SourceNode();
                    neighborNode.TitleNode = graph.TitleNode;
                    neighborNode.Source = source;
                    neighborNode.SourceNodes = new List<SourceNodeJoin>();
                    neighborNode.TopicNodes = new List<SourceTopicJoin>();

                    neighborNode = SearchService.SearchSourceInformation(neighborNode);
                    neighborNode.Name = SearchService.GetSourceName(source);

                    // Add to graph
                    graph.Sources.Add(source);

                    // Assign to corresponding topics/mediums
                    foreach (string medium in neighborNode.Mediums)
                    {
                        bool assigned = false;

                        foreach (TopicNode topic in graph.TitleNode.TopicNodes)
                        {
                            if (topic.Name == medium)
                            {
                                // Add relationship
                                SourceTopicJoin topicJoin = new SourceTopicJoin();
                                topicJoin.TopicNode = topic;
                                topicJoin.SourceNode = neighborNode;

                                topic.SourceNodes.Add(topicJoin);
                                neighborNode.TopicNodes.Add(topicJoin);

                                assigned = true;

                                break;
                            }
                        }

                        // If haven't found corresponding topic, then make new
                        if (!assigned)
                        {
                            // Create topic
                            TopicNode topic = new TopicNode();
                            topic.Name = medium;
                            topic.TitleNode = graph.TitleNode;
                            topic.SourceNodes = new List<SourceTopicJoin>();

                            // Create relationship
                            SourceTopicJoin topicJoin = new SourceTopicJoin();
                            topicJoin.TopicNode = topic;
                            topicJoin.SourceNode = neighborNode;

                            topic.SourceNodes.Add(topicJoin);
                            neighborNode.TopicNodes.Add(topicJoin);
                        }
                    }
                }

                // Recursively search neighboring node
                AddReferenceMedium(graph, neighborNode, depth, currDepth);
            }
        }

        private static void AddReferenceLocation(GraphNode graph, SourceNode currNode, int depth, int currDepth)
        {
            // Make sure not at max depth yet
            if (currDepth >= depth)
                return;

            currDepth++;

            List<string> references = SearchService.SearchReferences(currNode.Source);

            // Get all neighbors
            foreach (string source in references)
            {
                // Add relationship basis
                SourceNodeJoin nodeJoinParent = new SourceNodeJoin();
                SourceNodeJoin nodeJoinChild = new SourceNodeJoin();

                nodeJoinParent.SourceNode1 = currNode;
                nodeJoinChild.SourceNode2 = currNode;

                SourceNode neighborNode;

                // Check if source already exists
                if (graph.Sources.Contains(source))
                {
                    List<Node> path = GetPathBySource(graph, source);

                    neighborNode = (SourceNode)path[path.Count - 1]; // Get last element of path (found node)
                }
                else
                {
                    // Create new node
                    neighborNode = new SourceNode();
                    neighborNode.TitleNode = graph.TitleNode;
                    neighborNode.Source = source;
                    neighborNode.SourceNodes = new List<SourceNodeJoin>();
                    neighborNode.TopicNodes = new List<SourceTopicJoin>();

                    neighborNode = SearchService.SearchSourceInformation(neighborNode);
                    neighborNode.Name = SearchService.GetSourceName(source);

                    // Add to graph
                    graph.Sources.Add(source);

                    // Assign to corresponding topicNode
                    bool assigned = false;

                    foreach (TopicNode topic in graph.TitleNode.TopicNodes)
                    {
                        if (topic.Name == neighborNode.Location)
                        {
                            // Add relationship
                            SourceTopicJoin topicJoin = new SourceTopicJoin();
                            topicJoin.TopicNode = topic;
                            topicJoin.SourceNode = neighborNode;

                            topic.SourceNodes.Add(topicJoin);
                            neighborNode.TopicNodes.Add(topicJoin);

                            assigned = true;

                            break;
                        }
                    }

                    // If haven't found corresponding topic, then make new
                    if (!assigned)
                    {
                        // Create topic
                        TopicNode topic = new TopicNode();
                        topic.Name = neighborNode.Location;
                        topic.TitleNode = graph.TitleNode;
                        topic.SourceNodes = new List<SourceTopicJoin>();

                        // Create relationship
                        SourceTopicJoin topicJoin = new SourceTopicJoin();
                        topicJoin.TopicNode = topic;
                        topicJoin.SourceNode = neighborNode;

                        topic.SourceNodes.Add(topicJoin);
                        neighborNode.TopicNodes.Add(topicJoin);
                    }
                }

                // Recursively search neighboring node
                AddReferenceLocation(graph, neighborNode, depth, currDepth);
            }
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

        
        // GET PATH OF NODE BY SOURCE
        public static List<Node>? GetPathBySource(GraphNode graph, string source)
        {
            List<Node> path = new List<Node>();

            path.Add(graph.TitleNode);

            List<Node>? minPath = null;

            // Search every topic's connected source node
            foreach (TopicNode topic in graph.TitleNode.TopicNodes)
            {
                foreach (SourceTopicJoin sourceJoin in topic.SourceNodes) 
                {
                    SourceNode currNode = sourceJoin.SourceNode;

                    List<Node>? result = GetPathBySource(graph.TitleNode, source, currNode, path);

                    // Check if shortest path
                    if (result != null)
                    {
                        if (minPath != null)
                        {
                            if (result.Count < path.Count)
                                minPath = result;
                        } else
                        {
                            minPath = result;
                        }
                    }
                }
            }

            // Return result if exists
            return minPath;
        }

        // Recursively get path by source
        private static List<Node>? GetPathBySource(TitleNode titleNode, string source, SourceNode currNode, List<Node> path)
        {
            path.Add(currNode);

            if (source == currNode.Source)
                return path;

            List<Node>? minPath = null;

            foreach (SourceNodeJoin nodeJoin in currNode.SourceNodes)
            {
                SourceNode neighborNode = nodeJoin.SourceNode2;

                List<Node>? result = GetPathBySource(titleNode, source, neighborNode, path);

                // Check if shortest path
                if (result != null)
                {
                    if (minPath != null)
                    {
                        if (result.Count < path.Count)
                            minPath = result;
                    }
                    else
                    {
                        minPath = result;
                    }
                }
            }

            // Return smallest or null path
            return minPath;
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