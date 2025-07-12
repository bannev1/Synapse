using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Xml;

namespace api.Services
{
    public static class SearchService
    {
        // Search Google via API and get URL results
        public static List<string> SearchQuery(string query, string GoogleAPIkey, string engineID = "4454355756a844f0e", int amount = 10)
        {
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
    }
}
