import config 

from flask import Flask 
from sqlalchemy import create_engine
from flask_cors import CORS 

from model import UserDao, TweetDao
from service import UserService, TweetService