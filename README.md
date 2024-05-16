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

## API Documentation

This document provides documentation for the user management APIs.

### Create User

- **URL**: `/api/users/v1/create_user`
- **Method**: `POST`
- **Description**: Creates a new user in the database.
- **Request Body**:

    ```json
    {
        "name": "John Doe",
        "age": 30,
        "phone_number": "1234567890",
        "education": "Bachelor's Degree",
        "pincode": "12345"
    }
    ```

- **Response**:

    - **Success (201)**:

        ```json
        {
            "message": "User created successfully"
        }
        ```

    - **Error (400)**:

        ```json
        {
            "error": "Incomplete user data"
        }
        ```

        OR

        ```json
        {
            "error": "Invalid request body"
        }
        ```

    - **Error (500)**:

        ```json
        {
            "error": "Internal Server Error"
        }
        ```

### Get User

- **URL**: `/api/users/v1/get_user/<int:user_id>`
- **Method**: `GET`
- **Description**: Retrieves user details by ID from the database.
- **Parameters**:
    - `user_id`: Unique identifier of the user.
- **Response**:

    - **Success (200)**:

        ```json
        {
            "Unique_id": 1,
            "name": "John Doe",
            "age": 30,
            "phone_number": "1234567890",
            "education": "Bachelor's Degree",
            "pincode": "12345"
        }
        ```

    - **Error (404)**:

        ```json
        {
            "error": "User not found"
        }
        ```

    - **Error (500)**:

        ```json
        {
            "error": "Internal Server Error"
        }
        ```

### Update User

- **URL**: `/api/users/v1/update_user/<int:user_id>`
- **Method**: `PUT`
- **Description**: Updates user details by ID in the database.
- **Parameters**:
    - `user_id`: Unique identifier of the user.
- **Request Body**:

    ```json
    {
        "name": "John Doe",
        "age": 35,
        "phone_number": "9876543210",
        "education": "Master's Degree",
        "pincode": "54321"
    }
    ```

- **Response**:

    - **Success (200)**:

        ```json
        {
            "message": "User updated successfully"
        }
        ```

    - **Error (404)**:

        ```json
        {
            "error": "User not found"
        }
        ```

    - **Error (500)**:

        ```json
        {
            "error": "Internal Server Error"
        }
        ```

### Delete User

- **URL**: `/api/v1/users/delete_user/<int:user_id>`
- **Method**: `DELETE`
- **Description**: Deletes a user by ID from the database.
- **Parameters**:
    - `user_id`: Unique identifier of the user.
- **Response**:

    - **Success (200)**:

        ```json
        {
            "message": "User deleted successfully"
        }
        ```

    - **Error (404)**:

        ```json
        {
            "error": "User not found"
        }
        ```

    - **Error (500)**:

        ```json
        {
            "error": "Internal Server Error"
        }
        ```
Sure, here's the documentation for the provided code in Markdown format:

## Demographic Score Calculation

### 1. Function: `insert_train_data(age, education, pincode)`

This function inserts data into the database and automatically computes metrics based on the pincode.

- **Parameters**:
  - `age`: Age of the individual.
  - `education`: Education level of the individual.
  - `pincode`: Pincode of the area where the individual resides.

### 2. Function: `generate_train_data(n)`

This function generates training data by calling `insert_train_data()`.

- **Parameters**:
  - `n`: Number of data points to generate.

### 3. Function: `populate_district_info(conn)`

This function populates the `DistrictInfo` table by scraping data from a website.

- **Parameters**:
  - `conn`: SQLite database connection object.

### 4. Function: `create_users_table()`

This function creates the `Users` table in the database.

### 5. Function: `create_scores_table()`

This function creates the `Scores` table in the database.

### 6. Function: `create_creditworthiness_score_table()`

This function creates the `creditworthiness_score` table in the database.

### 7. Function: `create_district_info_table()`

This function creates the `DistrictInfo` table in the database and populates it with data.

### 8. Function: `create_train_table()`

This function creates the `TrainData` table in the database.

### 9. Function: `drop_table()`

This function drops the `Users` table from the database.

### 10. Function: `formula(age, edu, growth, literacy)`

This function computes a demographic score based on age, education level, district growth, and literacy rate.

- **Parameters**:
  - `age`: Age of the individual.
  - `edu`: Education level of the individual.
  - `growth`: Growth rate of the district.
  - `literacy`: Literacy rate of the district.

### 11. Function: `check_formula(formula)`

This function checks the `formula()` function by applying it to the data in the `TrainData` table and printing the results.

- **Parameters**:
  - `formula`: The demographic score calculation formula.