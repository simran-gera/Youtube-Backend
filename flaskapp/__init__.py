from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json, sys, os
from sqlalchemy import create_engine
from crypt import methods
from ctypes import addressof
from os import uname
import re
from flask import Flask, request, jsonify, redirect, url_for, Response
from flask.templating import render_template
from sqlalchemy.sql.functions import user
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
import hashlib, jwt
from flask import session
from functools import wraps
from sqlalchemy import func
import json, os
from inspect import signature

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@youtubedb/youtube"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

from flaskapp.models import Video, APIKey


db.create_all()
db.session.commit()

app.config["YOUTUBE_DATA_API_KEY"] = os.environ.get("YOUTUBE_DATA_API_KEY")


migrate = Migrate()
migrate.init_app(app, db)

from flaskapp import views
