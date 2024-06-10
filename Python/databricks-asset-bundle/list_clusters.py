import requests
import json

# Replace with your Databricks workspace URL and personal access token
workspace_url = "https://<azure databricks workspace url>"
token = "<token>"

headers = {"Authorization": f"Bearer {token}"}

# API endpoint URL
# url = f"{workspace_url}/api/2.0/clusters/list-node-types"
url = f"{workspace_url}/api/2.0/clusters/spark-versions"


# Send GET request
response = requests.get(url, headers=headers)

# Check for successful response
if response.status_code == 200:
  data = response.json()
  with open('list-spark-verions.json', 'w') as f:
    json.dump(data, f)
  print("Spark versions:", data)
else:
  print("Error:", response.status_code, response.text)
