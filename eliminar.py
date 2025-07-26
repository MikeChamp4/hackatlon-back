import requests
import json

url = "http://192.168.12.87:11434/api/generate"

payload = json.dumps({
  "model": "gemma:7b",
  "prompt": "Cual es la capital de brasil",
  "stream": False
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)