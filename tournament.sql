-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Connects to db and drops db if it exists
\c vagrant
drop database if exists tournament;

-- Creates new db
create database tournament;
\c tournament

-- creates new tables
create table players (
    id serial primary key,
    name text
    );

-- Creates table matches with primary key,
-- even though not used in application to conform
-- with normalized design pattern
create table matches (
    id serial primary key,
    winner integer,
    foreign key(winner) references players(id),
    loser integer,
    foreign key(loser) references players(id)
    );


-- Creates view that generates standings overview
create view standings as
    select players.id, players.name,
        (select count(*) from matches where players.id in (winner, loser)) as played,
        (select count(*) from matches where players.id = matches.winner) as won
    from players, matches
    group by players.id
    order by won desc;
