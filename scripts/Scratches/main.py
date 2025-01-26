import requests

url = "https://www.climatewatchdata.org/api/v1/ghg-emissions"
headers = {"Authorization": "Bearer YOUR_API_KEY"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()  # Parsowanie danych w formacie JSON
    print(data)
else:
    print(f"Błąd: {response.status_code}")