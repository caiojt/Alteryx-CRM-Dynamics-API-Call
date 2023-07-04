#################################
#################################
import requests
import pandas as pd
from ayx import Alteryx

def remove_null_columns(df):
    # Drop columns with all null values
    df = df.dropna(axis=1, how='all')

    return df

def call_crm_api(url, headers):
    try:
        response = requests.get(url, headers=headers,verify=False)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def fetch_all_data(api_url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = []
    next_link = api_url

    while next_link:
        response = call_crm_api(next_link, headers)
        data.extend(response['value'])
        next_link = response.get('@odata.nextLink')

    return data


api_url = "https://YOUR_SITE.crm.dynamics.com/api/data/v9.2/TABLE_YOU_WANT"
input1 = Alteryx.read('#1')
bearer_token = input1['security_token'].iloc[0]

all_data = fetch_all_data(api_url, bearer_token)
df = pd.json_normalize(all_data)
df = remove_null_columns(df)
#limits string columns to 100 cara
df = df.applymap(lambda x: x[:100] if isinstance(x, str) else x)
Alteryx.write(df,1)




#################################

