using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Xml;

using api.Models.Graph.Nodes;
using api.Environment;
using System.Globalization;

namespace api.Services
{
    public static class SearchService
    {
        // Search Google via API and get URL results
        public static List<string> SearchQuery(string query, string engineID = "4454355756a844f0e", int amount = 10)
        {
            // Get API key
            string GoogleAPIkey = Variables.GoogleAPIKey;

            HttpClient client = new HttpClient();
            query = Uri.EscapeDataString(query);

            string requestURL = $"https://www.googleapis.com/customsearch/v1?key={GoogleAPIkey}&cx={engineID}&q={query}&num={amount}";
            HttpResponseMessage response = client.GetAsync(requestURL).GetAwaiter().GetResult();

            if (!response.IsSuccessStatusCode)
                throw new HttpRequestException($"Google Search Failed: {response.StatusCode}");

            var json = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
            using var document = JsonDocument.Parse(json);
            var root = document.RootElement;
            var items = root.GetProperty("items");

            var urls = new List<string>();
            foreach (var item in items.EnumerateArray())
            {
                urls.Add(item.GetProperty("link").GetString()!);
            }

            return urls;
        }


        // Get topics as a list of strings from Wikipedia API
        public static List<string>? GetTopics(string query)
        {
            HttpClient client = new HttpClient();

            string url = $"https://en.wikipedia.org/w/api.php?action=parse&page={Uri.EscapeDataString(query)}&prop=sections&format=json";

            // Execute request
            HttpResponseMessage response = client.GetAsync(url).GetAwaiter().GetResult();

            if (!response.IsSuccessStatusCode)
            {
                throw new HttpRequestException($"Request failed: {response.StatusCode}");
            }

            // Parse JSON response
            string json = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
           
            List<string> headings = new List<string>();
            using JsonDocument document = JsonDocument.Parse(json);

            // Navigate JSON structure
            if (document.RootElement.TryGetProperty("parse", out JsonElement parse) &&
                parse.TryGetProperty("sections", out JsonElement sections))
            {
                foreach (JsonElement section in sections.EnumerateArray())
                {
                    if (section.TryGetProperty("line", out JsonElement line))
                    {
                        headings.Add(line.GetString()!);
                    }
                }
            }
            return headings;
        }


        // Get URLs referenced in webpage
        public static List<string> SearchReferences(string url)
        {
            // Download HTML content
            string html;
            using (var client = new WebClient())
            {
                client.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36");
                client.Encoding = System.Text.Encoding.UTF8;
                try
                {
                    html = client.DownloadString(url);
                }
                catch (WebException ex)
                {
                    throw new ApplicationException($"Failed to download webpage: {ex.Message}");
                }
            }

            // Extract links using regex
            var links = new List<string>();
            var baseUri = new Uri(url);
            var pattern = @"href\s*=\s*[""'](?<url>[^""'#]+)[""']";

            foreach (Match match in Regex.Matches(html, pattern, RegexOptions.IgnoreCase))
            {
                string rawUrl = match.Groups["url"].Value.Trim();

                // Skip problematic links
                if (string.IsNullOrWhiteSpace(rawUrl)) continue;
                if (rawUrl.StartsWith("javascript:", StringComparison.OrdinalIgnoreCase)) continue;
                if (rawUrl.StartsWith("mailto:", StringComparison.OrdinalIgnoreCase)) continue;
                if (rawUrl.StartsWith("tel:", StringComparison.OrdinalIgnoreCase)) continue;
                if (rawUrl.StartsWith("data:", StringComparison.OrdinalIgnoreCase)) continue;

                try
                {
                    // Convert to absolute URL
                    Uri absoluteUri = rawUrl.StartsWith("http", StringComparison.OrdinalIgnoreCase)
                        ? new Uri(rawUrl)
                        : new Uri(baseUri, rawUrl);

                    // Add only HTTP(S) URLs
                    if (absoluteUri.Scheme == Uri.UriSchemeHttp || absoluteUri.Scheme == Uri.UriSchemeHttps)
                    {
                        links.Add(absoluteUri.AbsoluteUri);
                    }
                }
                catch (UriFormatException)
                {
                    continue;
                }
            }

            // Return unique links
            return new HashSet<string>(links).ToList();
        }


        // Populate sourceNode information
        public static SourceNode SearchSourceInformation(SourceNode source, bool getMediums = true, bool getLocation = true)
        {
            // Validate environment variables
            string ip2LocationKey = Variables.IP2GeolocationAPIKey;
            string ipinfoToken = Variables.ipinfoAPIKey;

            // Populate Mediums using IP2Location API
            if (getMediums)
            {
                try
                {
                    string domain = new Uri(source.Source).Host;
                    string ip = "";

                    // DNS resolution directly in method
                    using (var dnsClient = new HttpClient())
                    {
                        string dnsUrl = $"https://dns.google/resolve?name={domain}&type=A";
                        var dnsResponse = dnsClient.GetAsync(dnsUrl).GetAwaiter().GetResult();
                        dnsResponse.EnsureSuccessStatusCode();

                        string dnsJson = dnsResponse.Content.ReadAsStringAsync().GetAwaiter().GetResult();
                        using (JsonDocument dnsDoc = JsonDocument.Parse(dnsJson))
                        {
                            if (dnsDoc.RootElement.TryGetProperty("Answer", out JsonElement answer))
                            {
                                foreach (JsonElement record in answer.EnumerateArray())
                                {
                                    if (record.TryGetProperty("type", out JsonElement type) &&
                                        type.GetInt32() == 1 &&
                                        record.TryGetProperty("data", out JsonElement data))
                                    {
                                        ip = data.GetString() ?? "";
                                        break;
                                    }
                                }
                            }
                        }
                    }

                    if (!string.IsNullOrEmpty(ip))
                    {
                        using (var client = new HttpClient())
                        {
                            string apiUrl = $"https://api.ip2location.io/?key={ip2LocationKey}&ip={ip}";
                            var response = client.GetAsync(apiUrl).GetAwaiter().GetResult();
                            response.EnsureSuccessStatusCode();

                            string json = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
                            using (JsonDocument doc = JsonDocument.Parse(json))
                            {
                                if (doc.RootElement.TryGetProperty("domain_category", out JsonElement category))
                                {
                                    string categoryName = category.GetString();
                                    if (!string.IsNullOrEmpty(categoryName))
                                    {
                                        // Map to media types
                                        source.Mediums = categoryName;
                                    }
                                }
                            }
                        }
                    }
                    else
                    {
                        source.Mediums = new List<string> { "website" };
                    }
                }
                catch
                {
                    source.Mediums = new List<string> { "website" };
                }
            }

            // Populate Location using DNS resolution and ipinfo.io
            if (getLocation)
            {
                try
                {
                    // Extract domain from URL
                    string domain = new Uri(source.Source).Host;
                    string ip = "";

                    // DNS resolution directly in method
                    using (var dnsClient = new HttpClient())
                    {
                        string dnsUrl = $"https://dns.google/resolve?name={domain}&type=A";
                        var dnsResponse = dnsClient.GetAsync(dnsUrl).GetAwaiter().GetResult();
                        dnsResponse.EnsureSuccessStatusCode();

                        string dnsJson = dnsResponse.Content.ReadAsStringAsync().GetAwaiter().GetResult();
                        using (JsonDocument dnsDoc = JsonDocument.Parse(dnsJson))
                        {
                            if (dnsDoc.RootElement.TryGetProperty("Answer", out JsonElement answer))
                            {
                                foreach (JsonElement record in answer.EnumerateArray())
                                {
                                    if (record.TryGetProperty("type", out JsonElement type) &&
                                        type.GetInt32() == 1 &&
                                        record.TryGetProperty("data", out JsonElement data))
                                    {
                                        ip = data.GetString() ?? "";
                                        break;
                                    }
                                }
                            }
                        }
                    }

                    // Get location from ipinfo.io
                    if (!string.IsNullOrEmpty(ip))
                    {
                        using (var ipClient = new HttpClient())
                        {
                            string ipUrl = $"https://ipinfo.io/{ip}/json?token={ipinfoToken}";
                            var ipResponse = ipClient.GetAsync(ipUrl).GetAwaiter().GetResult();
                            ipResponse.EnsureSuccessStatusCode();

                            string ipJson = ipResponse.Content.ReadAsStringAsync().GetAwaiter().GetResult();
                            using (JsonDocument ipDoc = JsonDocument.Parse(ipJson))
                            {
                                JsonElement root = ipDoc.RootElement;
                                string city = root.TryGetProperty("city", out JsonElement cityElem)
                                    ? cityElem.GetString() ?? "Unknown"
                                    : "Unknown";

                                string country = root.TryGetProperty("country", out JsonElement countryElem)
                                    ? countryElem.GetString() ?? "Unknown"
                                    : "Unknown";

                                source.Location = country; // only save country
                            }
                        }
                    }
                    else
                    {
                        source.Location = "Unknown";
                    }
                }
                catch
                {
                    source.Location = "Unknown";
                }
            }

            return source;
        }

        // Get name of source nodes using Wikipedia API
        public static string GetSourceName(string url)
        {
            try
            {
                // First extract domain from URL
                var uri = new Uri(url);
                string domain = uri.Host.ToLower();

                // Remove common prefixes and extract core domain
                string coreDomain = domain
                    .Replace("www.", "")
                    .Replace("blog.", "")
                    .Replace("news.", "")
                    .Split('.')[0];

                // Clean domain name for Wikipedia search
                string searchQuery = coreDomain
                    .Replace("-", " ")
                    .Replace("_", " ");
                searchQuery = CultureInfo.CurrentCulture.TextInfo.ToTitleCase(searchQuery);

                // Use Wikipedia API to find actual source name
                using (var client = new HttpClient())
                {
                    // Search Wikipedia for pages related to the domain
                    string apiUrl = $"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={Uri.EscapeDataString(searchQuery)}&format=json";
                    var response = client.GetAsync(apiUrl).GetAwaiter().GetResult();
                    response.EnsureSuccessStatusCode();

                    string json = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
                    using (JsonDocument doc = JsonDocument.Parse(json))
                    {
                        JsonElement root = doc.RootElement;
                        if (root.TryGetProperty("query", out JsonElement query) &&
                            query.TryGetProperty("search", out JsonElement search))
                        {
                            // Look for a result that matches our domain
                            foreach (JsonElement item in search.EnumerateArray())
                            {
                                if (item.TryGetProperty("title", out JsonElement titleElement))
                                {
                                    string title = titleElement.GetString();

                                    // Check if this is likely the correct source
                                    if (IsValidSourceName(title, coreDomain))
                                    {
                                        return title;
                                    }
                                }
                            }
                        }
                    }
                }

                // Fallback to domain extraction if Wikipedia search fails
                return GetSourceNameFromDomain(url);
            }
            catch
            {
                return "Unknown Source";
            }
        }

        private static bool IsValidSourceName(string title, string coreDomain)
        {
            // Skip disambiguation pages and lists
            if (title.Contains("(disambiguation)") || title.StartsWith("List of"))
                return false;

            // Check if title contains the domain keywords
            string cleanTitle = title.ToLower().Replace(" ", "");
            string cleanDomain = coreDomain.ToLower().Replace(" ", "");

            return cleanTitle.Contains(cleanDomain);
        }

        private static string GetSourceNameFromDomain(string url)
        {
            try
            {
                var uri = new Uri(url);
                string domain = uri.Host;

                // Remove common prefixes
                domain = domain.Replace("www.", "")
                              .Replace("blog.", "")
                              .Replace("news.", "");

                // Extract main domain name
                string[] parts = domain.Split('.');
                if (parts.Length > 1)
                {
                    string brand = parts[0];

                    // Clean up special characters
                    brand = brand.Replace("-", " ")
                                 .Replace("_", " ");

                    // Convert to title case
                    return CultureInfo.CurrentCulture.TextInfo.ToTitleCase(brand.ToLower());
                }
                return domain;
            }
            catch
            {
                return "Unknown Source";
            }
        }


        public static List<string> GetAutocompleteOptions(string query, int maxOptions)
        {
            List<string> options = new List<string>();

            using (var client = new HttpClient())
            {
                string url = $"https://en.wikipedia.org/w/api.php?action=query&format=json&assert=anon&list=prefixsearch&formatversion=2&pssearch={query}&pslimit={maxOptions}";
                var response = client.GetAsync(url).GetAwaiter().GetResult();
                response.EnsureSuccessStatusCode();

                string json = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
                using (JsonDocument doc = JsonDocument.Parse(json))
                {
                    JsonElement root = doc.RootElement;
                    if (root.TryGetProperty("query", out JsonElement queryRes) &&
                        queryRes.TryGetProperty("prefixsearch", out JsonElement search))
                    {
                        // Look for suggestion
                        foreach (JsonElement item in search.EnumerateArray())
                        {
                            if (item.TryGetProperty("title", out JsonElement titleElement))
                            {
                                string title = titleElement.GetString();

                                options.Add(title);
                            }
                        }
                    }
                }
            }

            return options;
        }
    }
}
