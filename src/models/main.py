from bs4 import BeautifulSoup
import requests
import Levenshtein

class User:
    """
    User gives his age, education, pincode.
    district is determined by pincode
    various features of the district are computed using census data
    these features are appended to the user data
    """


    def __init__(self, age, education, pincode):
        self.age = age
        self.education = education
        self.pincode = pincode
        self.POSTAL_URL = 'https://api.postalpincode.in/pincode'
        self.CENSUS_URL = 'https://www.census2011.co.in/district.php'

    def fetch_district(self):
        response = requests.get(f"{self.POSTAL_URL}/{self.pincode}")
        content = response.json()[0]['PostOffice'][0]
        return content['District']

    def fetch_district_literacy(self):
        page_number = 1
        district = self.fetch_district()
        flag = False
        rows = [0]

        print('Searching for', district)
        while len(rows) != 0:
            page = requests.get(f"{self.CENSUS_URL}?page={page_number}")
            soup = BeautifulSoup(page.content, "html.parser")
            rows = soup.find('table').findAll('tr')[1:]    
            for row in rows:
                row_data = row.findAll('td')
                row_district = row_data[1].text
                if Levenshtein.distance(row_district, district, weights=(1, 1, 5)) < max(len(row_district), len(district)) // 2:        
                    row_population = int(row_data[3].text.replace(',', ''))
                    row_growth = float(row_data[4].text.replace(' %', ''))
                    row_literacy = float(row_data[6].text) 
                    flag = True
                    break
            if flag == True:
                break
            
            page_number += 1    
        
        if flag == True:
            print(f"{row_district=}, {row_population=}, {row_growth=}, {row_literacy=}")
        else:
            print('District Not Found')

class Database:
    def __init__(self):
        self.db = []

    def add_user(self, user):
        self.db.append(user)

user = User(10, "H", 500049)
user.fetch_district()
user.fetch_district_literacy()

