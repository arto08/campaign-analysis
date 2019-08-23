'''
Created on Aug 20, 2019

@author: Arto
'''
import pandas as pd
from pandas.io.json import read_json
import time
source1 = "source1.csv"
source2 = "source2.csv"

df1 = pd.read_csv(source1)
df2 = pd.read_csv(source2)


"""prints how many campaigns spent more than a specified amount of days"""
def campaign_days(days):
    camp_date_group = df2.groupby(['campaign_id','date']).size().reset_index().rename(columns={0:'day_count'})
    total_days = camp_date_group.groupby('campaign_id').count()
    campaigns_above_limit = total_days[total_days['day_count'] > days]
    
    print 'number of campaigns that ran more than ' + str(days) + ' days'
    print len(campaigns_above_limit.index)
    print ''



def compare_action(action1, action2): 
    js = df2['actions'].apply(read_json)
    summary = pd.concat(js.tolist()).groupby('action', as_index=False).sum()
    two_actions = summary.loc[(summary['action']== action1) | (summary['action']==action2)]
    print 'the following sources had more ' + action1 + ' than ' + action2
    if action1==two_actions.iloc[0][0]: #checking the order of the actions in two_actions
        print two_actions[two_actions.columns[two_actions.iloc[(0)]>two_actions.iloc[(1)]]].columns.values
    else: 
        print two_actions[two_actions.columns[two_actions.iloc[(1)]>two_actions.iloc[(0)]]].columns.values
    print ''


def source_action_target(source, action, target):
    target = target+'_'
    target_df = df1.loc[df1['audience'].str.contains(target)][['campaign_id', 'audience']]
    camp_action = df2[['campaign_id', 'actions']]
    merged_df = target_df.merge(camp_action, on='campaign_id')
    js = merged_df['actions'].apply(read_json)
    summary = pd.concat(js.tolist()).groupby('action', as_index=False).sum()
  
    print 'number of ' + action + ' from source ' + source + ' targeted towards ' + target
    print summary.loc[summary['action'] == action][source]
    print ''

def cost_per_view():
    video_ads = df2[['ad_type', 'spend', 'actions']].loc[df2['ad_type'] == 'video']
    json_actions = video_ads['actions'].apply(read_json) #heavy operation. can definitely be parallelized 
    actions_summary = pd.concat(json_actions.tolist()).groupby('action', as_index=False).sum()
    total_views = actions_summary.loc[actions_summary['action'] == 'views'].sum(axis=1)
    total_spend = video_ads['spend'].sum()
    cost_per_view = total_spend/total_views
  
    print 'total cost per view' 
    print '%.2f'%(cost_per_view) 
    print ''

def lowest_CPM():
    spend = df2[['campaign_id', 'spend']]
    merged_df = df1.merge(spend, on='campaign_id')
    summary = merged_df.groupby(['campaign_id', 'audience', 'impressions'], as_index=False)['spend'].sum()
    summary['cpm'] = (summary['spend']/summary['impressions'])*1000
 
    print 'lowest CPM'
    print summary['cpm'].min()
    print ''
    
    
t0 = time.time()
campaign_days(4)
compare_action('junk', 'noise')
source_action_target("B","conversions","NY")
cost_per_view()
lowest_CPM()
t1 = time.time()
print 'total time spent in seconds: ' + str(t1-t0)