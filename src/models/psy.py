import requests
import json

resp = requests.get('http://127.0.0.1:5001/gen_questions', json={'Q1': "A",'A1': "A",'Q2': "A",'A2': "A",'Q3': "A",'A3': "A",'Q4': "A",'A4': "A",'Q5': "A",'A5': "A",'Q6': "A", 'A6': "A",'Q7': "A",'A7': "A",'Q8': "A",'A8': "A",'Q9': "A",'A9': "A",'Q10': "A",'A10': "A",})
data = json.loads(resp.json())
print(data)

resp = requests.get('http://127.0.0.1:5001/rate_answers', json={'Q1': "How rich are you?",'A1': "Very.",'Q2': "You responsible bro?",'A2': "Nah."})
data = json.loads(resp.json())
print(data["R1"], data["R2"])


