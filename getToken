#################################
import requests
from ayx import Alteryx
import pandas as pd

def call_api(url, data=None, headers=None):
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        data = response.json()
        token = data.get('access_token')
        return token
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

api_url = "https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token"
api_data = {
    "grant_type": "client_credentials",
    "client_id": "CLIENT_ID",
    "client_secret": "CLIENT_SECRET",
    "scope":"https://YOUR_SITE.api.crm.dynamics.com/.default"
}
api_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
form_encoded_data = "&".join([f"{key}={value}" for key, value in api_data.items()])

key = call_api(api_url, data=form_encoded_data, headers=api_headers)
df = pd.DataFrame({'security_token': [key]})
Alteryx.write(df,1)
