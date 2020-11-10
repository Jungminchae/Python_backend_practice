from flask import Flask, jsonify, request, Response
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text 
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS

@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user['password'] = bcrypt.hashpw(
        new_user['password'].encode('UTF-8'),
        bcrypt.gensalt()
    )
    new_user_id = app.database.execute(text("""
        insert into users (
            name,
            email,
            profile,
            hashed_password
        ) values(
            :name,
            :email,
            :profile,
            :password
        )
    """), new_user).lastrowid
    new_user_info = get_user(new_user_id)

    return jsonify(new_user_info)

@app.route('./login', methods=['POST'])
def login():
    credential = request.json
    email = credential['email']
    password = credential['password']

    row = database.execute(text("""
        select
            id,
            hashed_password
        from users
        where email = :email
    """), {'email' : email}).fetchall()

    if row and bcrypt.checkpw(password.encode('UTF-8'), row['hashed_password'].encode('UTF-8')):
        user_id = row['id']
        payload = {
            'user_id' : user_id
            'exp' : datetime.utcnow() + timedelta(seconds = 60 * 60 * 24)
        }
        token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], 'HS256')
        return jsonify({
            'access_token' : token.decode('UTF-8')
        })
    else:
        return ', 401'



@app.route('/tweet', methods=['POST'])
@login_required
def tweet():
    user_tweet = request.json
    user_tweet['id'] = g.user_id
    tweet = user_tweet['tweet']

    if len(tweet) > 300:
        return '300자를 초과했습니다.' 400
    insert_tweet(user_tweet)
    return "", 200

@app.route('/follow', methods=['POST'])
@login_required
def follow():
    payload = request.json 
    insert_follow(payload)
    return '', 200

@app.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
    payload = request.json 
    insert_unfollow(payload)
    return '', 200


@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    rows = app.database.execute(text("""
            select
                t.user_id,
                t.tweet
            from tweets t
            left join users_follow_list_url ON ufl.user_id = :user_id
            where t.user_id = :user_id
            OR t.user_id = ufl.follow_user_id
    """), {
        'user_id' : user_id
    }).fetchall()

    timeline = [{
        'user_id' : row['user_id'], 
        'tweet' : row['tweet']
    } for row in rows]

    return jsonify({
        'user_id' : user_id,
        'timeline' : timeline
    })


def create_app(test_config = None):
    app = Flask(__name__)
    
    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding= 'utf-8', max_overflow = 0)
    app.database = database

    return app
def get_user(user_id):
    user = current_app.database.execute(text("""
        select
        id,
        name,
        email,
        profile
        from users
        where id = :user_id
    """), {
        'user_id' : user_id
    }).fetchall()

def insert_user(user):
    return current_app.database.execute(text("""
            insert into users (
                name,
                email,
                profile,
                hashed_password
            ) values (
                :name,
                :email,
                :profile,
                :password
            )
    """), user).lastrowid

def insert_tweet(user_tweet):
    return current_app.database.execute(text("""
            insert into tweets (
                user_id,
                tweet
            ) values (
                :id,
                :tweet
            )
    """), user_tweet).rowcount

def insert_follow(user_follow):
    return current_app.database.execute(text(
        """
            insert into users_follow_list (
                user_id,
                follow_user_id
            ) values(
                :id,
                :follow
            )
        """
    ), user_follow).rowcount

def insert_unfollow(user_unfollow):
    return current_app.database.execute(text(
        """ 
            delete from users_follow_list
            where user_id = :id
            and follow_user_id = :unfollow
        """
    ), user_unfollow).rowcount

def get_timeline(user_id):
    timeline = current_app.database.execute(text("""
        select
        t.user_id,
        t.tweet
        from tweets t
        left join users_follow_list ufl on ufl.user_id = :user_id
        where t.user_id = :user_id
        or t.user_id = ufl.follow_user_id
    """), {
        'user_id' : user_id
    }).fetchall()

    return [{
            'user_id' : tweet['user_id'],
            'tweet' : tweet['tweet']
    } for tweet in timeline]

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)


### test
# def test_decorator(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         print('Decorated Function')
#         return f(*args, **kwargs)
#     return decorated_function

# @test_decorator
# def func():
#     print('Calling funct function')

def login_required(f):
    @wraps(f)
    def decorated_function(*arg, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            try:
                payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], 'HS256')
            except jwt.InvalidTokenError:
                payload = None 
            
            if payload is None : return Response(status=401):
            
            user_id = payload['user_id']
            g.user_id = user_id
            g.user = get_user_info(user_id) if user_id else None 
        else:
            return Response(status= 401)
        
        return f(*args, **kwargs)
    return decorated_function

