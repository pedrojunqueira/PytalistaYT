client_id = ""  # Replace with your Azure AD app's client ID
client_secret = ""  # Replace with your Azure AD app's client secret
tenant_id = ""  # Replace with your Azure AD tenant ID
authority = f"https://login.microsoftonline.com/{tenant_id}"
base_url = "https://api.fabric.microsoft.com/v1/"

# Scopes for Fabric APIs
scopes = [      
    "https://api.fabric.microsoft.com/.default"  # Use .default for client credentials flow
]

import msal
import requests


def get_authentication_app():
    """
    Function to create and return a MSAL ConfidentialClientApplication instance.
    This is used for acquiring tokens using client credentials flow.
    """
    return msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority
    )


def get_access_token():
    """
    Function to acquire an access token using client credentials flow.
    Returns the access token if successful, otherwise returns None.
    """
    result = get_authentication_app().acquire_token_for_client(scopes=scopes)
    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"Error: {result.get('error_description', 'No token acquired')}")
        return None
    
def get_workspaces(token):
    """
    Function to get the list of workspaces.
    Returns the response text if successful, otherwise returns None.
    """
    if token:
        client = requests.Session()
        client.headers.update({"Authorization": f"Bearer {token}"})
        response = client.get(f"{base_url}workspaces")
        if response.ok:
            return response.json()["value"]
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            return None
    return None


def create_lakehouse(workspace_id, lakehouse_name):
    """
    Function to create a lakehouse in the specified workspace.
    Returns the response text if successful, otherwise returns None.
    """
    token = get_access_token()
    if token:
        client = requests.Session()
        client.headers.update({"Authorization": f"Bearer {token}"})
        url = f"{base_url}workspaces/{workspace_id}/lakehouses"
        payload = {
            "displayName": lakehouse_name,
            "description": "Sample Lakehouse"
        }
        response = client.post(url, json=payload)
        if response.ok:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            return None
    return None


if __name__ == "__main__":
    token = get_access_token()
    # print(token)
    # ws = get_workspaces(token)
    # print(ws)
    r = create_lakehouse("911a299c-19c5-4eef-9e18-d2d6a723f6b4", "demo_lakehouse")
    print(r)