-- Create database
CREATE DATABASE synapse;

\c synapse;

-- Clear database
DROP TABLE IF EXISTS cacheTopicSourceJoinTable;
DROP TABLE IF EXISTS savedTopicSourceJoinTable;
DROP TABLE IF EXISTS cacheSourceSourceJoinTable;
DROP TABLE IF EXISTS savedSourceSourceJoinTable;
DROP TABLE IF EXISTS cacheSourceNodes;
DROP TABLE IF EXISTS savedSourceNodes;
DROP TABLE IF EXISTS cacheTopicNodes;
DROP TABLE IF EXISTS savedTopicNodes;
DROP TABLE IF EXISTS cache;
DROP TABLE IF EXISTS saved;
