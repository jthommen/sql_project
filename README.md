# sql_project
SQL Project for the Udacity full-stack Web Developer course

## Features
`tournament.sql`
* Initial database instructions
* Defines database
* Defines tables
* Defines views


`tournament.py`
* Python functions to:
  * connect to db
  * Register players
  * Register matches
  * Delete players
  * Delete matches
  * Inquire standings/scores
  * Generate new matching for upcoming rounds
 
 
 `tournament_test.sql`
 * Test suite to check functionality of tournament.py 


### To run locally:
1. Install vagrant
2. Install virtual machine (vm) with psql, python 2.7
3. Start vagrant from vm folder with `vagrant up`
4. Log into vm with `vagrant ssh`
5. Fire up PostgreSQL with `psql`
6. Import initial database scheme with `\i tournament.sql`
7. In another terminal window run `python tournament_test.py`
