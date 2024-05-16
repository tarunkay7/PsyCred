import requests
import json

def send_prompt():
    # Define the URL and headers
    url = 'https://api.hyperleap.ai/prompts'
    headers = {
        'Content-Type': 'application/json',
        'x-hl-api-key': 'OWQ0MmI1YTdjOTQxNDUyNGFmODBmMDBhZmM5ZGMwYzU='  # Replace with your API key
    }

    # Define the JSON data
    data = {
        "promptId": "31764ccc-cff7-4590-8898-e87b2aa905dd",
        "promptVersionId": "d70a9468-f798-4d00-af57-c6523250501e",
        "replacements": {
            "Q1": "Q1 value",
            "A1": "A1 value",
            "Q2": "Q2 value",
            "A2": "A2 value",
            "Q3": "Q3 value",
            "A3": "A3 value",
            "Q4": "Q4 value",
            "A4": "A4 value",
            "Q5": "Q5 value",
            "A5": "A5 value",
            "Q6": "Q6 value",
            "A6": "A6 value",
            "Q7": "Q7 value",
            "A7": "A7 value",
            "Q8": "Q8 value",
            "A8": "A8 value",
            "Q9": "Q9 value",
            "A9": "A9 value",
            "Q10": "Q10 value",
            "A10": "A10 value"
        }
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the response status code is OK (200)
    if response.status_code == 200:
        # Attempt to parse the response as JSON
        try:
            response_data = response.json()
            return response_data
        except json.JSONDecodeError:
            return {'error': 'Invalid JSON response from the server'}
    else:
        return {'error': f'Request failed with status code {response.status_code}'}

# Example usage
response_data = send_prompt()
print(response_data)
