#######################################################################################
#######################################################################################
#######################################################################################
# Original Author: Mark Stowell                                                       #
# Date Created: 6-3-22                                                                #
# Date of Last Modification: 6-3-22                                                   #
# Description:                                                                        #
#   This program will extract all primary youtube comments from a given youtube       #
#   video (determined by videoId).                                                    #
#                                                                                     #
#   To use this code, simply alter the variable videoId to the desired youtube        #
#   video's videoId and run the code.                                                 #
#######################################################################################
#######################################################################################
#######################################################################################

from googleapiclient.discovery import build
from dotenv import load_dotenv
from pprint import pprint
import win32com.client as win32 
import json
import os


# Create youtube api client using build(...) method: this allows us to utilize the YouTube API.
# .env file helps mask API Key (place this file in .gitignore)
# Example .env file contents:
#   YOUTUBE_API_KEY=insert_YouTube_API_Key_here_without_quotes
#   
#   Note: do not put a space before/after the assignment operator (=)
#   Accessing this "variable" is shown below through os module with getenv(...) method. This is similar to dictionary/accessing key-value pair.
load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)


# Set videoId and first run request
# This is the value we alter to retrieve results for a desired video.
videoId = 'yRA0KMCEP2o'
request = youtube.commentThreads().list(part='id, snippet', videoId=videoId, maxResults='100')
response = request.execute()


# Extract nextPageToken to run request again on next set of comments - max 100 comments per "page", must use nextPageToken
# to extract the next 100 comments

try:
    nextPageToken = response['nextPageToken']
except:
    nextPageToken = None

rows = []

for record in response['items']:
    userId = record['id']
    threadKind = record['kind']
    canReply = record['snippet']['canReply']
    isPublic = record['snippet']['isPublic']
    topLevelCommentKind = record['snippet']['topLevelComment']['kind']
    commentAuthorChannelId = record['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
    commentAuthorChannelUrl = record['snippet']['topLevelComment']['snippet']['authorChannelUrl']
    commentAuthorDisplayName = record['snippet']['topLevelComment']['snippet']['authorDisplayName']
    commentAuthorProfileImageUrl = record['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']
    commentCanRate = record['snippet']['topLevelComment']['snippet']['canRate']
    commentLikeCount = record['snippet']['topLevelComment']['snippet']['likeCount']
    commentPublishedAt = record['snippet']['topLevelComment']['snippet']['publishedAt']
    commentTextDisplay = record['snippet']['topLevelComment']['snippet']['textDisplay']
    commentTextOriginal = record['snippet']['topLevelComment']['snippet']['textOriginal']
    commentUpdatedAt = record['snippet']['topLevelComment']['snippet']['updatedAt']
    commentViewerRating = record['snippet']['topLevelComment']['snippet']['viewerRating']
    commentTotalReplyCount = record['snippet']['totalReplyCount']
    videoId = record['snippet']['videoId']
    rows.append([threadKind, canReply, isPublic, topLevelCommentKind, commentAuthorChannelId, commentAuthorChannelUrl, commentAuthorDisplayName, commentAuthorProfileImageUrl, commentCanRate, commentLikeCount, commentPublishedAt, commentTextOriginal, commentUpdatedAt, commentViewerRating, commentTotalReplyCount, userId, videoId, commentTextDisplay])


"""
Repeat this process on successive pages of a given youtube video (max 100 comments per page, must use nextPageToken to extract
more than the first 100 comments)
"""
# count is not necessary, but can be helpful to limit the number of iterations in the while loop
# Each iteration costs 1 api token returning 100 comments per iteration
# If a video contains a very large number of comments (>100k), it will come at a high API token cost without a count control.
# If you wish to control, simply add another condition in the while loop (i.e. while nextPageToken and count < 20)  
count = 0
while nextPageToken:
    print(nextPageToken)
    pageToken = nextPageToken
    request = youtube.commentThreads().list(part='id, snippet', videoId=videoId, maxResults='100', pageToken=pageToken)
    response = request.execute()

    for record in response['items']:
        try:
            userId = record['id']
            threadKind = record['kind']
            canReply = record['snippet']['canReply']
            isPublic = record['snippet']['isPublic']
            topLevelCommentKind = record['snippet']['topLevelComment']['kind']
            commentAuthorChannelId = record['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
            commentAuthorChannelUrl = record['snippet']['topLevelComment']['snippet']['authorChannelUrl']
            commentAuthorDisplayName = record['snippet']['topLevelComment']['snippet']['authorDisplayName']
            commentAuthorProfileImageUrl = record['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']
            commentCanRate = record['snippet']['topLevelComment']['snippet']['canRate']
            commentLikeCount = record['snippet']['topLevelComment']['snippet']['likeCount']
            commentPublishedAt = record['snippet']['topLevelComment']['snippet']['publishedAt']
            commentTextDisplay = record['snippet']['topLevelComment']['snippet']['textDisplay']
            commentTextOriginal = record['snippet']['topLevelComment']['snippet']['textOriginal']
            commentUpdatedAt = record['snippet']['topLevelComment']['snippet']['updatedAt']
            commentViewerRating = record['snippet']['topLevelComment']['snippet']['viewerRating']
            commentTotalReplyCount = record['snippet']['totalReplyCount']
            videoId = record['snippet']['videoId']
            rows.append([threadKind, canReply, isPublic, topLevelCommentKind, commentAuthorChannelId, commentAuthorChannelUrl, commentAuthorDisplayName, commentAuthorProfileImageUrl, commentCanRate, commentLikeCount, commentPublishedAt, commentTextOriginal, commentUpdatedAt, commentViewerRating, commentTotalReplyCount, userId, videoId, commentTextDisplay])
        except:
            None
    try:
        nextPageToken = response['nextPageToken']
    except:
        nextPageToken = None
    count += 1
    
"""
Step 2 Inserting Record to an Excel Spreadsheet
"""

ExcelApp = win32.Dispatch('Excel.Application')
ExcelApp.Visible = True

wb = ExcelApp.Workbooks.Add()
ws = wb.Worksheets(1)

header_labels = ('threadKind', 'canReply', 'isPublic', 'topLevelCommentKind', 'commentAuthorChannelId', 'commentAuthorChannelUrl', 'commentAuthorDisplayName', 'commentAuthorProfileImageUrl', 'commentCanRate', 'commentLikeCount', 'commentPublishedAt', 'commentTextOriginal', 'commentUpdatedAt', 'commentViewerRating', 'commentTotalReplyCount', 'userId', 'videoId', 'commentTextDisplay')

#Insert headers

for indx, val in enumerate(header_labels):
    ws.Cells(1, indx + 1).Value = val

#Insert records
row_tracker = 2
column_size = len(header_labels)

for row in rows:
    ws.Range(
        ws.Cells(row_tracker, 1),
        ws.Cells(row_tracker, column_size)
        ).value = row
    row_tracker += 1

