from enum import unique
from flask import Flask
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json, sys, os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime
from flaskapp import db


class Video(db.Model):
    __tablename__ = "video"

    _id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.String(1250))
    url = db.Column(db.String(250),default='wY6UyatwVTA')
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)
    thumbnail = db.Column(db.String(250))

class APIKey(db.Model):
    __tablename__ = "apikey"

    key = db.Column(db.String(), primary_key=True)
    limit_over = db.Column(db.Boolean, default=False, nullable=False)

    def __str__(self):
        return self.key