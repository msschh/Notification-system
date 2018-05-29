import requests


URL = 'http://127.0.0.1:10000'

def get_groups(is_admin, is_teacher):
    groups_url = None
    if is_admin == 1:
        groups_url = URL + '/resources'
    if is_teacher == 1:
        groups_url = URL + '/resources_teacher'

    json_resp = requests.get(url=groups_url)

    return json_resp.json()