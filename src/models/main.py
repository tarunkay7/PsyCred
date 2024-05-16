from bs4 import BeautifulSoup
import requests

class User:
    def __init__(self, age, education, pincode):
        self.age = age
        self.education = education
        self.pincode = pincode
        self.district_literacy = None        
        self.district = None    


    def fetch_state_district(self):
        response = requests.get(f"https://api.postalpincode.in/pincode/{self.pincode}")
        content = response.json()[0]['PostOffice'][0]
        self.state = content['State']
        if self.state == 'Telangana':
            self.state = 'Andhra Pradesh'
        self.district = content['District']

        print(content)


    def fetch_state_literacy(self):
        url = 'https://www.census2011.co.in/states.php'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find('table')
        rows = table.findAll('tr')
        for row in rows[2:]:
            row_data = row.findAll('td')

            state = row_data[1].text
            population = row_data[2].text
            growth = row_data[3].text
            literacy = row_data[7].text 
            
            if state.lower() == self.state.lower():
                print(f"{state=}, {population=}, {growth=}, {literacy=}")

    def fetch_district_literacy(self):
        url = 'https://www.census2011.co.in/district.php'
    

class Database:
    def __init__(self):
        self.db = []

    def add_user(self, user):
        self.db.append(user)

user = User(10, "H", 500049)
user.fetch_state_district()
user.fetch_state_literacy()

d

