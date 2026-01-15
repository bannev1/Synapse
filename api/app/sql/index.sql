-- File to configure tables in database

-- Enable UUID extension (required for generating UUIDs for saved graphs)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";



-- CACHE TABLE (equiv to a GraphNode/TitleNode)
CREATE TABLE cache (
	id SERIAL PRIMARY KEY,
	query VARCHAR(8000) NOT NULL,
	graphType VARCHAR(20) CHECK (graphType IN ('source', 'topic', 'title')) NOT NULL,
	sources VARCHAR(8000) NOT NULL, -- CSV list of sources
	timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);


-- SAVED GRAPH TABLE (equiv to a GraphNode/TitleNode)
CREATE TABLE saved (
	id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	name VARCHAR(8000) NOT NULL,
	depth INT NOT NULL,
	graphType VARCHAR(20) CHECK (graphType IN ('source', 'topic', 'title')) NOT NULL
);

-----------------------
-- GRAPH STORAGE TABLES
-----------------------

-- Colors Storage Table (for easier use)
CREATE TABLE colors (
	colorValue VARCHAR(100) PRIMARY KEY
);


-- CACHE GRAPH TABLES

-- Source nodes table for cache
CREATE TABLE cacheSourceNodes (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES cache(id) ON DELETE CASCADE,
	name VARCHAR(5000) NOT NULL,
	color VARCHAR(100) REFERENCES colors(colorValue) NOT NULL,
	source VARCHAR(5000) NOT NULL,
	location VARCHAR(3000) NOT NULL,
	mediums VARCHAR(8000) NOT NULL -- CSV list of mediums
);

-- Topic nodes table for cache
CREATE TABLE cacheTopicNodes (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES cache(id) ON DELETE CASCADE,
	name VARCHAR(5000) NOT NULL,
	color VARCHAR(100) REFERENCES colors(colorValue) NOT NULL
);

-- Join Table for cache source/topic nodes
CREATE TABLE cacheTopicSourceJoinTable (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES cache(id) ON DELETE CASCADE,
	topicNode INT REFERENCES cacheTopicNodes(id) ON DELETE CASCADE,
	sourceNode INT REFERENCES cacheSourceNodes(id) ON DELETE CASCADE
);

-- Join Table for cache source/source nodes
CREATE TABLE cacheSourceSourceJoinTable (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES cache(id) ON DELETE CASCADE,
	sourceNode1 INT REFERENCES cacheSourceNodes(id) ON DELETE CASCADE,
	sourceNode2 INT REFERENCES cacheSourceNodes(id) ON DELETE CASCADE
);


-- SAVED GRAPH TABLES

-- Source nodes table for saved graphs
CREATE TABLE savedSourceNodes (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES saved(id) ON DELETE CASCADE,
	name VARCHAR(500) NOT NULL,
	color VARCHAR(100) REFERENCES colors(colorValue) NOT NULL,
	source VARCHAR(5000) NOT NULL,
	location VARCHAR(3000) NOT NULL,
	mediums VARCHAR(8000) NOT NULL -- CSV list of mediums
);

-- Topic nodes table for saved graphs
CREATE TABLE savedTopicNodes (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES saved(id) ON DELETE CASCADE,
	name VARCHAR(5000) NOT NULL,
	color VARCHAR(100) REFERENCES colors(colorValue) NOT NULL
);

-- Join Table for saved graph source/topic nodes
CREATE TABLE savedTopicSourceJoinTable (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES cache(id) ON DELETE CASCADE,
	topicNode INT REFERENCES savedTopicNodes(id) ON DELETE CASCADE,
	sourceNode INT REFERENCES savedSourceNodes(id) ON DELETE CASCADE
);

-- Join Table for saved source/source nodes
CREATE TABLE savedSourceSourceJoinTable (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES cache(id) ON DELETE CASCADE,
	sourceNode1 INT REFERENCES savedSourceNodes(id) ON DELETE CASCADE,
	sourceNode2 INT REFERENCES savedSourceNodes(id) ON DELETE CASCADE
);
