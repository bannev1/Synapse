using api.Data;
using api.Models;
using api.Models.Graph;

namespace api.Controllers
{
    public class CacheController
    {
        private readonly DataContext _dataContext;

        public CacheController(DataContext dataContext)
        {
            _dataContext = dataContext;
        }

        public GraphNode? GetCachedGraph(string query, string graphType)
        {
            // Search if cached
            Cache? cachedGraph = _dataContext.Caches.Where(c => c.Query == query && c.GraphType == graphType)
                .OrderByDescending(c => c.Timestamp)
                .FirstOrDefault();

            // Refresh cache for next time
            this.RefreshCache();

            // Check if cached graph found
            if (cachedGraph != null)
                return cachedGraph.Graph;

            // Otherwise return null
            return null;
        }

        public void RefreshCache()
        {
            // Remove all entries older than 24 hours
            DateTime threshold = DateTime.UtcNow.AddHours(-24);
            var oldEntries = _dataContext.Caches.Where(c => c.Timestamp < threshold).ToList();
            foreach (var entry in oldEntries)
            {
                _dataContext.Caches.Remove(entry);
            }
            _dataContext.SaveChanges();
        }
    }
}
