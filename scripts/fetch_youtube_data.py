import os
import pandas as pd
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def fetch_youtube_comments(api_key, video_ids):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    comments_data = []
    for video_id in video_ids:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        )
        response = request.execute()
        
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments_data.append({
                'video_id': video_id,
                'comment_text': comment['textDisplay'],
                'author': comment['authorDisplayName'],
                'likes': comment['likeCount'],
                'timestamp': comment['publishedAt']
            })
    
    return pd.DataFrame(comments_data)

# Example training data structure
training_data = {
    'comment_text': [
        "This product is amazing! Great features",
        "Terrible customer service, very disappointed",
        "Decent product but expensive for what you get",
        "Love the new update, much better performance"
    ],
    'sentiment': [
        'positive',
        'negative',
        'neutral',
        'positive'
    ]
}

# Save as CSV for training
pd.DataFrame(training_data).to_csv('data/training_data.csv', index=False)
