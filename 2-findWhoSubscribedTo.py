#######################################################################################
#######################################################################################
#######################################################################################
# Original Author: Mark Stowell                                                       #
# Date Created: 6-3-22                                                                #
# Date of Last Modification: 6-3-22                                                   #
# Description:                                                                        #
#   This program is intended for use with datasets extracted from YouTube API.        #
#   The intent of this program, specifically, is to gather subscription data          #
#   for users based on their channelId (i.e. we want to find all channels a           #
#   user is subscribed to).                                                           #
#                                                                                     #
# Limitation:                                                                         #
#   Some users restrict what is shared on their account(s). Thus, attempting          #
#   to extract subscription data from such users will result in an error/no reponse   #
#   from the API. This is accounted for in the code, the data cell for such users     #
#   will hold [], an empty list.                                                      #
#######################################################################################
#######################################################################################
#######################################################################################

from googleapiclient.discovery import build
from dotenv import load_dotenv
import win32com.client as win32 
import pandas as pd
import os
import json

load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)

# Read in dataset stored in excel spreadsheet and store in Pandas data frame. 
df = pd.read_excel('currentdata.xlsx')

# Our final list of subscribers where each row represents the subscribed channels corresponding to the row
# in currentdata.xlsx. 
subscribed_list = []

for x in range(len(df)):
    channels_subscribed = []
    channelId = df.loc[x]['commentAuthorChannelId']
    request = youtube.subscriptions().list(part='snippet', channelId=channelId, maxResults='500')
    
    # First try-except: catches subscriptionsForbidden error (i.e. user has no subscriptions) and 
    #                   no items found error (user does not have any subscriptions)
    #
    # Note: in the event of one of the above errors, the current iteration's data cell will be set to []. 
    #       We then skip the iteration (continue statement) and proceed with the to the next channelId.
    try:
        response = request.execute()
    except:
        subscribed_list.append(channels_subscribed)
        continue
    
    # Using count variable to limit the results to max ~500 subscribed channels: 
    # Some users may have more than 500 subscriptions, each subscrpition API request (nextPageToken) 
    # requires 1 quota per request - can become very costly if no limit placed.
    count = 0
    for record in response['items']:
        try:
            subscribed_channel = record['snippet']['resourceId']['channelId']
            channels_subscribed.append(subscribed_channel)
            count += 1
        except:
            None

    try:
        nextPageToken = response["nextPageToken"]
    except:
        print("first attempt: no page token found")
        nextPageToken = None
    while nextPageToken is not None and count < 500:
        print(nextPageToken)
        request = youtube.subscriptions().list(part='snippet', channelId=channelId, maxResults='250', pageToken = nextPageToken)
        response = request.execute()

        for record in response['items']:
            try:
                subscribed_channel = record['snippet']['resourceId']['channelId']
                channels_subscribed.append(subscribed_channel)
                count += 1
            except:
                print("No subscription info")
        try:
            nextPageToken = response["nextPageToken"]
        except:
            nextPageToken = None

    subscribed_list.append(channels_subscribed)


df_test = pd.DataFrame(columns = {'SubscribedChannels'})
for x in range(len(subscribed_list)):
    df_test.at[x, 'SubscribedChannels'] = subscribed_list[x]
print(df_test)

df_test.to_excel('test.xlsx')