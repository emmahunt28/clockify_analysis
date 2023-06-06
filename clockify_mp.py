import pendulum
import pandas as pd 
import numpy as np
import requests

key = "MDAxZDE4YmUtZmQwNy00MzllLWFiYzQtM2JjM2M5NTMzNTVl"
url = 'https://api.clockify.me/api/v1'
reporturl = 'https://reports.api.clockify.me/v1'
workspaceId = '63ada8fc28d7584d0c563d3f'


def get_summary(period='week'):
  lastweek_st = pendulum.today(tz='UTC').subtract(weeks=1).start_of('week')
  lastweek_end = lastweek_st.end_of('week')
  last_month_st = pendulum.today(tz='UTC').subtract(months=1).start_of('month')
  last_month_end = last_month_st.end_of('month')
  if period =='week':
    st = lastweek_st
    et = lastweek_end
  elif period =='month':
    st = last_month_st
    et = last_month_end
  else:
    print('incorrect period, use week or month only.')
    raise TypeError
  
  weekdays = np.busday_count(st.to_date_string(), et.to_date_string() )
  
  sumparam = { "dateRangeStart": st.to_iso8601_string(),
    "dateRangeEnd": et.to_iso8601_string(),
      "summaryFilter": {
      "groups": [
        "USER",
        "PROJECT",
        "TAG"
      ],},'amountShown':'HIDE_AMOUNT'}

  r = requests.post(reporturl +f'/workspaces/{workspaceId}/reports/summary',headers={'X-Api-Key':key},json=sumparam)
  summary = r.json()
  return summary,weekdays

def make_df(summary):
  # for each person: 
  p_sum = []
  for user in summary['groupOne']:
      for project_summary in user['children']:
          for tag in project_summary['children']:
              if 'name' in project_summary.keys():
                  tag['project'] = project_summary['name']
              else:
                  tag['project'] = None
              tag['user'] = user['name']
              tag['tag_name'] = tag['name']
              
              p_sum.append(tag)

  df = pd.DataFrame(p_sum)
  return df

def calc_util(df):
   # check for utilisation
    indirect_projects = [ 'Meetings', 'Admin', 'Training (Corporate)','Training (Corporate)','Recruitment']
    outof_scope = ['Holiday' , 'Bank Holiday','Sick Leave', 'Medical Appointment']
    team = ['Talia Solel', 'Toby Crisford','Matt Pang', 'Ben Collins','Ella Zheng', 'Emma Hunt','Georgi Pavlovski','Kieran Clarke']
    direct_stuff = df[~((df.project.isin(indirect_projects)) | (df.project.isin(outof_scope)))&(df.user.isin(team))]
    indirect_stuff = df[((df.project.isin(indirect_projects)) & ~ (df.project.isin(outof_scope)))&(df.user.isin(team))]
    totalh = pd.concat([direct_stuff,indirect_stuff]).groupby(['user'])['duration'].sum()/3600
    dhours = direct_stuff.groupby(['user'])['duration'].sum()/3600
    idhours = indirect_stuff.groupby(['user'])['duration'].sum()/3600
    util_percent = (dhours/totalh*100)
    # blank = pd.Series(np.zeros(len(team)),index=team)
    # util_percent = (blank+util_percent).fillna(0)
    team_util = dhours.sum()/totalh.sum()*100
    # print('Team utilisation %:',np.round(team_util,1))

    lhours = df[df.user.isin(team)].groupby(['user'])['duration'].sum()/3600
    blank = pd.Series(np.zeros(len(team)),index=team)
    teamhours = (blank+lhours).fillna(0)

    return team_util, util_percent, teamhours



def full_summary(period):
   sraw,weekdays = get_summary(period=period)
   print('weekdays',weekdays)
   s = make_df(sraw)
   team_util, util_percent,teamhours =  calc_util(s)
   print(team_util)
   print(util_percent)
   print(teamhours)


if __name__ == '__main__':
   full_summary('month')