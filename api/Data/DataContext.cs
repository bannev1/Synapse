using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

using api.Models;
using api.Models.Graph;
using api.Models.Graph.Nodes;
using api.Models.Graph.Nodes.Relationships;

namespace api.Data
{
	public class DataContext : DbContext
	{
		public DataContext (DbContextOptions<DataContext> options)
			: base(options)
		{ }

		// Graph
		public DbSet<GraphNode> GraphNodes { get; set; }
		public DbSet<SourceNode> SourceNodes { get; set; }
		public DbSet<TopicNode> TopicNodes { get; set; }
		public DbSet<TitleNode> TitleNodes { get; set; }

		// Relationships
		public DbSet<SourceTopicJoin> SourceTopicJoins { get; set; }
		public DbSet<SourceNodeJoin> SourceNodeJoins { get; set; }

		// Share
		public DbSet<ShareGraph> ShareGraphs { get; set; }
		// Cache
		public DbSet<Cache> Caches { get; set; }

		protected override void OnModelCreating(ModelBuilder modelBuilder)
		{
			base.OnModelCreating(modelBuilder);

			// Graph Entities/Models
			modelBuilder.Entity<GraphNode>()
				.HasKey(g => g.id);
			modelBuilder.Entity<GraphNode>()
				.HasOne<TitleNode>(g => g.TitleNode);

			modelBuilder.Entity<SourceNode>()
				.HasKey(s => s.id);
			modelBuilder.Entity<SourceNode>()
				.HasOne<TitleNode>(s => s.TitleNode);

			modelBuilder.Entity<TopicNode>()
				.HasKey(t => t.id);
            modelBuilder.Entity<TopicNode>()
                .HasOne<TitleNode>(t => t.TitleNode);

			modelBuilder.Entity<TitleNode>()
                .HasKey(t => t.id);
            modelBuilder.Entity<TitleNode>()
                .HasOne<GraphNode>(t => t.GraphNode);

            // Relationships
            modelBuilder.Entity<SourceTopicJoin>()
                .HasKey(stj => stj.id);
			modelBuilder.Entity<SourceTopicJoin>()
				.HasOne<SourceNode>(stj => stj.SourceNode);
			modelBuilder.Entity<SourceTopicJoin>()
                .HasOne<TopicNode>(stj => stj.TopicNode);

			modelBuilder.Entity<SourceNodeJoin>()
				.HasKey(snj => snj.id);
			modelBuilder.Entity<SourceNodeJoin>()
                .HasOne<SourceNode>(snj => snj.SourceNode1);
            modelBuilder.Entity<SourceNodeJoin>()
                .HasOne<SourceNode>(snj => snj.SourceNode2);

			// Share Entities
			modelBuilder.Entity<ShareGraph>()
				.HasKey(sg => sg.id);
			modelBuilder.Entity<ShareGraph>()
				.HasOne<GraphNode>(sg => sg.Graph);

			// Cache Entities
			modelBuilder.Entity<Cache>()
				.HasKey(c => c.id);
			modelBuilder.Entity<Cache>()
				.HasOne<GraphNode>(c => c.Graph);
        }
    }
}
