import sqlite3


def create_users_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('db/psy.db')
    cursor = conn.cursor()

    # Define the SQL statement to create the Users table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Users (
        Unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        age INTEGER CHECK (age > 18),
        phone_number TEXT UNIQUE,
        pincode INTEGER
    );
    '''

    try:
        # Execute the SQL statement to create the table
        cursor.execute(create_table_query)
        print("Table 'Users' created successfully.")
    except sqlite3.Error as e:
        print("Error creating table:", e)

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def create_scores_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('db/psy.db')
    cursor = conn.cursor()

    # Define the SQL statement to create the Scores table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Scores (
        user_id INTEGER,
        demographic_score DECIMAL DEFAULT 0,
        psychometric_test_score DECIMAL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES Users(Unique_id)
    );
    '''

    try:
        # Execute the SQL statement to create the table
        cursor.execute(create_table_query)
        print("Table 'Scores' created successfully.")
    except sqlite3.Error as e:
        print("Error creating table:", e)

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def create_creditworthiness_score_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('db/psy.db')
    cursor = conn.cursor()

    # Define the SQL statement to create the creditworthiness_score table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS creditworthiness_score (
        user_id INTEGER PRIMARY KEY,
        creditworthiness_score DECIMAL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES Users(Unique_id)
    );
    '''

    try:
        # Execute the SQL statement to create the table
        cursor.execute(create_table_query)
        print("Table 'creditworthiness_score' created successfully.")
    except sqlite3.Error as e:
        print("Error creating table:", e)

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def create_district_info_table():
    conn = sqlite3.connect('db/psy.db')
    cursor = conn.cursor()
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS DistrictInfo (
            district TEXT,
            population INTEGER,
            growth DECIMAL,
            sex_ratio INTEGER
            literacy_rate DECIMAL
        );
        '''
    try:
        # Execute the SQL statement to create the table
        cursor.execute(create_table_query)
        print("Table  created successfully.")
    except sqlite3.Error as e:
        print("Error creating table:", e)

    conn.commit()
    conn.close()
