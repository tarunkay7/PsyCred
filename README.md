# PsyCred

This is the official Repo for PsyCred during the 30 Hour Hackathon "MATHack"

link: https://github.com/tarunkay7/PsyCred

## Git Guide for Team

There are 4 essential commands you use in Git which are 

- `git add PATH/TO.FILE` : Adds the file to the staging area
- `git commit -m "COMMIT MESSAGE"` : Commits the file 
- `git push -u origin` : Pushes the file to remote repo
- `git pull` : Pulls changes from report repo

## Database Schema

### Users Table

The `Users` table stores information about users.

| Column Name | Data Type       | Constraints                | Description                     |
|-------------|-----------------|----------------------------|---------------------------------|
| Unique_id   | INTEGER         | PRIMARY KEY, AUTOINCREMENT | Unique identifier for each user|
| name        | VARCHAR         |                            | Name of the user                |
| age         | INTEGER         | CHECK (age > 18)           | Age of the user (must be over 18)|
| phone_number| TEXT            | UNIQUE                     | Phone number of the user        |
| pincode     | INTEGER         |                            | Pincode of the user             |

### Scores Table

The `Scores` table stores scores related to users.

| Column Name           | Data Type | Constraints           | Description                                   |
|-----------------------|-----------|-----------------------|-----------------------------------------------|
| user_id               | INTEGER   |                       | Foreign key referencing the Unique_id column in the Users table |
| demographic_score     | DECIMAL   | DEFAULT 0             | Score representing user's demographic data    |
| psychometric_test_score| DECIMAL   | DEFAULT 0             | Score representing user's psychometric test performance |

### creditworthiness_score Table

The `creditworthiness_score` table stores creditworthiness scores of users.

| Column Name           | Data Type | Constraints           | Description                                   |
|-----------------------|-----------|-----------------------|-----------------------------------------------|
| user_id               | INTEGER   | PRIMARY KEY           | Primary key referencing the Unique_id column in the Users table |
| creditworthiness_score| DECIMAL   | DEFAULT 0             | Score representing user's creditworthiness    |

### Foreign Key Constraints

- The `user_id` column in the `Scores` table references the `Unique_id` column in the `Users` table.
- The `user_id` column in the `creditworthiness_score` table references the `Unique_id` column in the `Users` table.

This schema is designed to store user information, including demographic details, psychometric test scores, and creditworthiness scores. Foreign key constraints ensure referential integrity between related tables.
