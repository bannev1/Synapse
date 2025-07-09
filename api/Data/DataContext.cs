using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using static Microsoft.EntityFrameworkCore.DbLoggerCategory.Database;

using api.Models;
using api.Models.Graph;
using api.Models.Graph.Nodes;

namespace api.Data
{
	public class DataContext : DbContext
	{
		public DataContext (DbContextOptions<DataContext> options)
			: base(options)
		{ }

		public DbSet<ShareGraph> Searches => Set<ShareGraph>();
		// For searches
		public DbSet<GraphNode> GraphNodes { get; set; }
		public DbSet<Node> Nodes { get; set; }
		public DbSet<SourceNode> SourceNodes { get; set; }
		public DbSet<TopicNode> TopicNodes { get; set; }
		public DbSet<TitleNode> TitleNodes { get; set; }

		protected override void OnModelCreating(ModelBuilder modelBuilder)
		{
			base.OnModelCreating(modelBuilder);

			modelBuilder.Entity<ShareGraph>()
				.HasKey(sg => sg.id);

			modelBuilder.Entity<ShareGraph>()
				.HasOne(sg => sg.Graph)
				.WithOne()
				.HasForeignKey<GraphNode>(g => g);

			modelBuilder.Entity<GraphNode>()
				.HasKey(gn => gn.id);

			modelBuilder.Entity<GraphNode>()
		}
	}
}
