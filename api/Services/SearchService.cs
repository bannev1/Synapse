using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace api.Services
{
    public static class SearchService
    {
        // Search Google via API and get URL results
        public static List<string> SearchURLs(string query, string GoogleAPIkey, string engineID = "4454355756a844f0e", int amount = 10)
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
    }
}
