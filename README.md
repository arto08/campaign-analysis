# campaign-analysis

Small project using pandas to get some insight about ad campaigns.

### data sources:

- source1.csv: campaign_id,audience,impressions
- source2.csv: ad_id,ad_type,campaign_id,date,spend,actions 

##### Some explaination on the data:
- a campaign has an audience, and is unique on ID
- an ad belongs to a campaign, has a type, and is unique on ID
- impressions in source1 are for the entire campaign
- stats in source2 are for the ad date
- {'a':17, 'action':'views'} means source A had 17 views 
- cost per view should only include ads of type VIDEO
- cost per view = video spend / video views
- CPM = spend / impressions * 1000

### 5 functions, each giving some insight about the data:

 - **campaign_days(days)**:    How many campaigns spent more than a specified amount of days. 

 - **compare_action(action1, action2)**: Which sources reported more of action1 than action2. 

- **source_action_target(source, action, target)**:  How many actions of the type 'action' from 'source' and target took place.  With source=B, action=conversions and target=NY, we give the number of conversations from source B targeted for NY.

 - **cost_per_view()**: Total cost per view (cost per view = video spend / video views) for all ads of type video, truncated to two decimals.

 - **lowest_CPM()**: What combination of state and hair color had the best (lowest) CPM (CPM = spend / impressions * 1000).


*compare_action*, *source_action_target* and *cost_per_view* all make use of .apply(read_json), which is a heavy operation where each JSON string from sounce2 is converted into a DataFrame. This slows down the runtime significantly. One could have a pre-processing step where this was done only once. It could also be parallelized in a production environment. To be able to run and not wait, one can simply
call .head(100) to work on a smaller subset of the DataFrame.

- python version 2.7
- pandas version 0.19
