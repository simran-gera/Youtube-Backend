from functools import wraps
import asyncio
import imp
from flaskapp import app, db
from crypt import methods
from ctypes import addressof
from os import uname
import re
from flask import Flask, request, jsonify, redirect, url_for, Response
from flask.templating import render_template
from sqlalchemy.sql.functions import user
from flaskapp.models import Video, APIKey
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
import hashlib, jwt
from flask import session
from functools import wraps
from sqlalchemy import func
import json, os
from inspect import signature
from apiclient.discovery import build
import queue 
import threading
from datetime import datetime, timedelta
from time import sleep


YOUTUBE_DATA_API_KEY = app.config["YOUTUBE_DATA_API_KEY"]
youtube = build('youtube','v3',developerKey = YOUTUBE_DATA_API_KEY)
ROWS_PER_PAGE = 5
CHECK_INTERVAL = 300 

q = queue.Queue()


def myqueue():
    def worker():
        while True:
            fetch_data()
            sleep(CHECK_INTERVAL)

    # turn-on the worker thread
    threading.Thread(target=worker, daemon=True).start()

    # block until all tasks are done
    q.join()


thread = threading.Thread(target=myqueue)
thread.start()

def fetch_data():    

    #querying the videos with thier video_id
    api_keys = APIKey.query.filter_by(limit_over=False)

    if not len(api_keys):
        return {}
    
    YOUTUBE_DATA_API_KEY = api_keys[0]

    target_ts = (
                datetime.now() - timedelta(seconds=CHECK_INTERVAL)
    ).isoformat() + "Z"
    try:
        r = youtube.search().list(q='software engineeer',part='snippet',type='video', maxResults=10, key=YOUTUBE_DATA_API_KEY, publishedAfter=target_ts,order="date")
        res = r.execute()

        
        results = res['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'key' : YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 10
        }

        ids = ','.join(video_ids)

        # querying infromation about the videos

        r = youtube.videos().list(part = "snippet", id = ids, maxResults = 10)
        res = r.execute()

        results = res['items']

        
        for result in results:
            video_data = Video(
                
                video_id = result['id'],
                title = result['snippet']['title'],
                description = result['snippet']['description'],
                url = f'https://www.youtube.com/watch?v={ result["id"] }',
                upload_time = result['snippet']['publishedAt'],
                thumbnail = result['snippet']['thumbnails']['high']['url']
            )
            #storing the new video data into the database
            db.session.add(video_data)
            db.session.commit()
    except:
        api_keys[0].limit_over = True
        api_keys[0].save()
        return {}


def async_action(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped


# Renders Home Page
@app.route("/")
def home():
    q.put(block=False, item=1)
    page = request.args.get('page', 1, type=int)
    if request.form:
        results = Video.query.filter(Video.title.ilike("%"+request.form['search']+"%")).order_by(Video.upload_time.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
    else:
        results = Video.query.order_by(Video.upload_time.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)     
        return render_template("/index.html",message=results)

@app.route("/add_api_key/<api_key>")
def add_api_key(api_key):
    print("IN API KEY BLOCK")
    print("API KET", api_key)
    if api_key is not None:
        entry = APIKey(
                key = api_key
            )
    db.session.add(entry)
    db.session.commit()
    return "DATA ADDEDD SUCESSFULLy"



@app.route("/", methods=["POST"])
@async_action
async def get_video():
    page = request.args.get('page', 1, type=int)
    if request.form['submit'] == 'all_videos':
        results = Video.query.order_by(Video.upload_time.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)     

    else:
        results = Video.query.filter(Video.title.ilike("%"+request.form['search']+"%")).order_by(Video.upload_time.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template("/index.html",message=results)


# Renders Error Handling Page
@app.errorhandler(Exception)
def handle_error(e):
    code = 404
    if isinstance(e, HTTPException):
        code = e.code
    return render_template("/error404.html")

