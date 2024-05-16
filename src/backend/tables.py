

from bs4 import BeautifulSoup
import requests
import Levenshtein
import sqlite3
import random
import numpy as np

def insert_train_data(age, education, pincode):
    """
    Inserts data into the database
    Automatically computes metrics based on pincode
    """

    conn = sqlite3.connect('psy.db')
    def get_data_from_pincode(pincode, conn):
        def pincode_to_district(pincode):
            POSTAL_URL = 'https://api.postalpincode.in/pincode'
            response = requests.get(f"{POSTAL_URL}/{pincode}")
            content = response.json()[0]['PostOffice'][0]
            return content['District']
        district = pincode_to_district(pincode)
        c = conn.cursor()
        c.execute('SELECT * FROM DistrictInfo')
        table = c.fetchall()
        best_score = 100
        best_row = None
        for row in table:        
            score = Levenshtein.distance(row[0], district, weights=(1, 1, 5))
            if score < best_score:
                best_score = score
                best_row = row
        return best_row
    district, population, growth, sex_ratio, literacy = get_data_from_pincode(pincode, conn)
    cursor = conn.cursor()

    query = f'''
        INSERT INTO TrainData
        (age, education, district, population, growth, sex_ratio, literacy)
        VALUES
        ({age}, '{education}', '{district}', {population}, {growth}, {sex_ratio}, {literacy})
    '''    

    cursor.execute(query)
    cursor.close()
    conn.commit()
    conn.close()

def generate_train_data(n):
    def gen_age():
        rand = 0
        while rand < 18 or rand > 92:
            rand = int(np.random.normal(38, 10))
        return rand
    def gen_edu():
        edu = ['H', 'B', 'M', 'P']
        return random.choice(edu)
    def is_valid_pin(pin):
        POSTAL_URL = 'https://api.postalpincode.in/pincode'
        response = requests.get(f"{POSTAL_URL}/{pin}")
        if (response.json()[0]['Status'] == 'Success'):
            return True
        else:
            print('Failed Pin', pin, response.json())
            return False
        
    def gen_pin():
        pin = "000000"
        while not is_valid_pin(pin):
            pin_first3 =  f"{random.randint(100, 900):03}"
            nums = [f"{num:03}" for num in range(901)]
            weights = [1 / (i + 1) for i in range(901)]
            pin_last3 = random.choices(nums, weights=weights, k=1)[0]
            pin = pin_first3 + pin_last3 
        return pin
    
    for i in range(n):
        print('Inserting', i)
        insert_train_data(gen_age(), gen_edu(), gen_pin())

generate_train_data(100)

def populate_district_info(conn):
    CENSUS_URL = 'https://www.census2011.co.in/district.php'
    page_number = 1
    rows = [0]
    cursor = conn.cursor()

    while len(rows) != 0:
        page = requests.get(f"{CENSUS_URL}?page={page_number}")
        soup = BeautifulSoup(page.content, "html.parser")
        rows = soup.find('table').findAll('tr')[1:]    
        for row in rows:
            row_data = row.findAll('td')

            row_district = row_data[1].text
            row_population = int(row_data[3].text.replace(',', ''))
            row_growth = float(row_data[4].text.replace(' %', ''))
            row_sex_ratio = int(row_data[5].text)
            row_literacy = float(row_data[6].text) 

            query = f'''
                INSERT INTO DistrictInfo
                (district, population, growth, sex_ratio, literacy_rate)
                VALUES
                ('{row_district}', {row_population}, {row_growth}, {row_sex_ratio}, {row_literacy})
            '''

            cursor.execute(query)

        page_number += 1    

    cursor.close()


def create_users_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('psy.db')
    cursor = conn.cursor()

    # Define the SQL statement to create the Users table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS Users (
        Unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        age INTEGER CHECK (age > 18),
        phone_number TEXT UNIQUE,
        education TEXT,
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
    conn = sqlite3.connect('psy.db')
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
    conn = sqlite3.connect('psy.db')
    cursor = conn.cursor()
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS DistrictInfo (
            district TEXT,
            population INTEGER,
            growth DECIMAL,
            sex_ratio INTEGER,
            literacy_rate DECIMAL
        );
        '''
    try:
        # Execute the SQL statement to create the table
        cursor.execute(create_table_query)
        print("Table  created successfully.")
    except sqlite3.Error as e:
        print("Error creating table:", e)
    
    populate_district_info(conn)
    
    conn.commit()
    conn.close()

def create_train_table():
    conn = sqlite3.connect('psy.db')
    cursor = conn.cursor()
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS TrainData (
            age INTEGER,
            education VARCHAR,
            district VARCHAR,
            population INTEGER,
            growth DECIMAL,
            sex_ratio INTEGER,
            literacy DECIMAL
        );
        '''
    try:
        cursor.execute(create_table_query)
        print("Table  created successfully.")
    except sqlite3.Error as e:
        print("Error creating table:", e)
        
    conn.commit()
    conn.close()

def drop_table():
    conn = sqlite3.connect('psy.db')
    cursor = conn.cursor()
    create_table_query = '''
    DROP TABLE Users
           '''
    try:
        cursor.execute(create_table_query)
        print("Table deleted successfully.")
    except sqlite3.Error as e:
        print("Error deleting table:", e)

    conn.commit()
    conn.close()
