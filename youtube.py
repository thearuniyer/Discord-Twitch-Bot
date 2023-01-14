from contextlib import nullcontext
from datetime import datetime
import os
from sys import api_version
from turtle import title
from webbrowser import get
import googleapiclient.discovery
import urllib.request
import json
import codecs

with open("config.json") as config_file:
    config = json.load(config_file)

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = config["youtube_apiKey"]

online_users = {}


def is_user_live(userId):
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        channelId=userId,
        eventType="live",
        type="video"
    )

    response = request.execute()

    return response


def get_yt_notifications():
  notifications = []
  
  for channel in config["yt_channels"]:
    info = is_user_live(channel)
    items = info["items"]
    # channel is added to exist with current time weather live or not
    if channel not in online_users:
      online_users[channel] = datetime.utcnow()
      
    # it means user is not live, add time is None
    if not items:
      online_users[channel] = None
      print("{} is not live " + channel)
    # user is live then calculate start time
    else:
      started_at = datetime.strptime(items[0]["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
      print("{} is live " + channel)
      if online_users[channel] is None or started_at > online_users[channel]:
        if online_users[channel] is None:
          print("adding notification because time was None")
        elif started_at > online_users[channel]:
          print("adding notification because started_at > utcnow_time")
        print("i am appending something")
        notifications.append(items[0])
        print("I appended something")
        online_users[channel] = started_at
        print("I changed time")

  return notifications