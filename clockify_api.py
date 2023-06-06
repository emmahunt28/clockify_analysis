# we want to use the API to post some time entries. 
# start by grabbing the entries for myself.
#
api_key = 'MDk1N2E0MzctNDY3Ni00NDIzLWJlZjMtMzM3YTU5NzkzNTQ2'

import requests
import pprint
base = 'https://api.clockify.me/api/v1'
# r = requests.get(url=base+'/user',headers={"X-Api-Key":api_key})
# #pprint.pprint(r.json())

# # for i,key in enumerate(json):
# #     print(json[i]['name'],json[i]['id'])
# #exit()
workspace_id = '63ada8fc28d7584d0c563d3f'
user_id = '63ce8b45f090c652269f98ba'

r = requests.get(url=base+f'/workspaces/{workspace_id}/user/{user_id}/time-entries',headers={"X-Api-Key":api_key})

json = r.json()
print(json)

# do one day.
import pendulum

# for the month of Feb. Populate all week days. 
# 
themonth= 3

this_day = pendulum.datetime(year=2023,month=4,day=15, hour = 9, minute = 0, second = 0)
format_date = this_day.to_iso8601_string()

project = '63e0c84ae057bd203264fc84'
tag_id = '63aee0ada3e51625ef0813d8'


for i in range(31):
    newday = this_day.add(days=i)
    if (newday.month == themonth) and (newday.weekday()<5):

        date_end = newday.add(hours=8).to_iso8601_string()

    # print(format_date,date_end)
        message = {'start': newday.to_iso8601_string(), 'end' : date_end, 'projectId' : project, 'tagIds' : [tag_id],"billable":"false","description":""}
        print(message)
        m = requests.post(url=base+f'/workspaces/{workspace_id}/time-entries',headers={"X-Api-Key":api_key},json=message)
    #print(m.json())