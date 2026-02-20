-- File to configure tables in database

-- Enable UUID extension (required for generating UUIDs for saved graphs)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";



-- CACHE TABLE (equiv to a GraphNode/TitleNode)
CREATE TABLE IF NOT EXISTS cache (
	id SERIAL PRIMARY KEY,
	query VARCHAR(100) NOT NULL,
	graphType VARCHAR(20) CHECK (graphType IN ('topical', 'medium', 'locational')) NOT NULL,
	depth int NOT NULL,
	timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);


-- SAVED GRAPH TABLE (equiv to a GraphNode/TitleNode)
CREATE TABLE IF NOT EXISTS saved (
	id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	name VARCHAR(100) NOT NULL,
	graphType VARCHAR(25) NOT NULL
);

-----------------------
-- GRAPH STORAGE TABLES
-----------------------


-- CACHE GRAPH TABLES

-- Source nodes table for cache
CREATE TABLE IF NOT EXISTS cacheSourceNodes (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES cache(id) ON DELETE CASCADE,
	name VARCHAR(500) NOT NULL,
	source VARCHAR(1000) NOT NULL,
	sourceName VARCHAR(250) NOT NULL,
	location VARCHAR(30) NOT NULL,
	medium VARCHAR(25) NOT NULL, 
	topics VARCHAR(1500) NOT NULL -- CSV list of topics
);

-- Topic nodes table for cache
CREATE TABLE IF NOT EXISTS cacheTopicNodes (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES cache(id) ON DELETE CASCADE,
	name VARCHAR(5000) NOT NULL
);

-- Join Table for cache source/topic nodes
CREATE TABLE IF NOT EXISTS cacheTopicSourceJoinTable (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES cache(id) ON DELETE CASCADE,
	topicNode INT REFERENCES cacheTopicNodes(id) ON DELETE CASCADE,
	sourceNode INT REFERENCES cacheSourceNodes(id) ON DELETE CASCADE
);

-- Join Table for cache source/source nodes
CREATE TABLE IF NOT EXISTS cacheSourceSourceJoinTable (
	id SERIAL PRIMARY KEY,
	graph INT REFERENCES cache(id) ON DELETE CASCADE,
	sourceNode1 INT REFERENCES cacheSourceNodes(id) ON DELETE CASCADE,
	sourceNode2 INT REFERENCES cacheSourceNodes(id) ON DELETE CASCADE
);


-- SAVED GRAPH TABLES

-- Source nodes table for saved graphs
CREATE TABLE IF NOT EXISTS savedSourceNodes (
	id SERIAL PRIMARY KEY,
	graph UUID REFERENCES saved(id) ON DELETE CASCADE,
	name VARCHAR(500) NOT NULL,
	source VARCHAR(1000) NOT NULL,
	sourceName VARCHAR(250) NOT NULL,
	location VARCHAR(30) NOT NULL,
	medium VARCHAR(25) NOT NULL,
	topics VARCHAR(1500) NOT NULL -- CSV list of topics
);

-- Topic nodes table for saved graphs
CREATE TABLE IF NOT EXISTS savedTopicNodes (
	id SERIAL PRIMARY KEY,
	graph UUID REFERENCES saved(id) ON DELETE CASCADE,
	name VARCHAR(5000) NOT NULL
);

-- Join Table for saved graph source/topic nodes
CREATE TABLE IF NOT EXISTS savedTopicSourceJoinTable (
	id SERIAL PRIMARY KEY,
	graph UUID REFERENCES saved(id) ON DELETE CASCADE,
	topicNode INT REFERENCES savedTopicNodes(id) ON DELETE CASCADE,
	sourceNode INT REFERENCES savedSourceNodes(id) ON DELETE CASCADE
);

-- Join Table for saved source/source nodes
CREATE TABLE IF NOT EXISTS savedSourceSourceJoinTable (
	id SERIAL PRIMARY KEY,
	graph UUID REFERENCES saved(id) ON DELETE CASCADE,
	sourceNode1 INT REFERENCES savedSourceNodes(id) ON DELETE CASCADE,
	sourceNode2 INT REFERENCES savedSourceNodes(id) ON DELETE CASCADE
);
