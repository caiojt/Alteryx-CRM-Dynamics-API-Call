#Calls Tableau API and fetches workbooks and views for a given site. After that it saves to a DataFrame in Alteryx.

from ayx import Alteryx
import tableauserverclient as TSC
import pandas as pd
import json

url = '#you_url#'
token_name = '#token_name#'
token_secret = '#you_secret#'
sitename = '#site_name#'
# Initialize an empty DataFrame
json_objects = []
view_objects = []

def authenticateTableau(server_url, mytoken_name, mytoken_secret, site):

    server = TSC.Server(server_url)
    server.add_http_options({'verify': False})
    server.use_server_version()
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=mytoken_name, personal_access_token=mytoken_secret, site_id=site)
    with server.auth.sign_in_with_personal_access_token(tableau_auth):
        print('[Logged in successfully to {}]'.format(server_url))
    server.auth.sign_in(tableau_auth)
    for wb in TSC.Pager(server.workbooks):
        json_obj = {"project_id":wb.project_id,"project_name":wb.project_name,"id": wb.id,"name": wb.name, "url": wb.webpage_url,"tags":list(wb.tags)}
        json_objects.append(json_obj)
    json_array = json.dumps(json_objects)

    for view in TSC.Pager(server.views):
        view_obj = {"project_id":view.project_id,"workbook_id":view.workbook_id,"id":view.id,"name":view.name,"url":view.content_url}
        view_objects.append(view_obj)
    view_array = json.dumps(view_objects)

    server.auth.sign_out()
    return json_array,view_array

response = authenticateTableau(url,token_name,token_secret,sitename)

# Create a Pandas DataFrame from the JSON data

workbooks , views = response
df_workbooks = pd.DataFrame(json.loads(workbooks))
df_views = pd.DataFrame(json.loads(views))

Alteryx.write(df_workbooks,1)
Alteryx.write(df_views,2)
