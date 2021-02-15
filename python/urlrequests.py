# pip3 install requests
import requests

url = "https://www.google.com"

response = requests.get(url)
print(f"{response.status_code} = {url}")
print(f"{response.text}")
