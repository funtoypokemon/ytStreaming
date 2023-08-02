#!/usr/bin python3
from datetime import date, datetime
import datetime
import json
import logging
from pprint import pformat
import sys
from time import sleep
import requests
from config import config
from kafka import KafkaProducer


def fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
        "key": google_api_key,
        "playlist_id": youtube_playlist_id,
        "part": "contentDetails",
        # "maxResults": 20,
        "pageToken": page_token,
    })
    
    payload = json.loads(response.text)

    logging.debug("Got %s", payload)

    return payload


def fetch_video_page(google_api_key, video_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/videos", params={
        "key": google_api_key,
        "id": video_id,
        "part": "snippet, statistics",
        "pageToken": page_token,
    })

    payload = json.loads(response.text)
    logging.debug("Got %s", payload)

    return payload


def fetch_playlist_items(google_api_key, youtube_playlist_id, page_token=None):
    payload = fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token)
    
    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from fetch_playlist_items(google_api_key, youtube_playlist_id, next_page_token)


def fetch_videos(google_api_key, youtube_playlist_id, page_token=None):
    payload = fetch_video_page(google_api_key, youtube_playlist_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token is not None:
        yield from fetch_video_page(google_api_key, youtube_playlist_id, page_token)


def summarize_video(video):

    return {
        "video_id": video["id"],
        "title": video["snippet"]["title"],
        "views": int(video["statistics"].get("viewCount", 0)),
        "likes": int(video["statistics"].get("likeCount", 0)),
        "comments": int(video["statistics"].get("commentCount", 0)),
        "input_time": str(datetime.datetime.now()),
    }


def on_delivery(err, record):
    pass

def main():
    sleep(15)
    logging.info("START") 

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer = lambda x:json.dumps(x).encode('utf-8'))

    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]

    for video_item in fetch_playlist_items(google_api_key, youtube_playlist_id):
        video_id = video_item["contentDetails"]["videoId"]
        for video in fetch_videos(google_api_key, video_id):
            logging.info("\n \nGOT %s", pformat(summarize_video(video)))

            mydata = {
                    "VIDEO_ID": video["id"],
                    "TITLE": video["snippet"]["title"],
                    "VIEWS": int(video["statistics"].get("viewCount", 0)),
                    "COMMENTS": int(video["statistics"].get("commentCount", 0)),
                    "LIKES": int(video["statistics"].get("likeCount", 0)),
                    "DATE": str(datetime.datetime.now()),
                }
            producer.send(
                topic="youtube_videos",
                # key = video_id,
                value = mydata
            )
            sleep(5)

    producer.flush()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
