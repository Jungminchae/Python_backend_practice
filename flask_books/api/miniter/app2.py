from flask import Flask, jsonify, request
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text 




@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
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

    row = current_app.database.execute(text("""
            select 
            id,
            name,
            email,
            profile
            from users
            where id = :user_id
    """), {
        'user_id' : new_user_id
    }).fetchone()

    create_user = {
        'id' : row['id'],
        'name' : row['name'],
        'email' : row['email'],
        'profile' : row['profile']
    } if row else None 
    return jsonify(create_user)

@app.route('/tweet', methods=['POST'])
def tweet():
    user_tweet = request.json
    tweet = user_tweet['tweet']

    if len(tweet) > 300:
        return '300자를 초과했습니다.' 400
    app.database.execute(text("""
        insert into tweets (
            uesr_id,
            tweet
        ) values(
            :id,
            :tweet
        )
    """), user_tweet)

    return "", 200

@app.route('/follow', methods=['POST'])
def follow():
    payload = request.json 
    insert_follow(payload)
    return '', 200

@app.route('/unfollow', methods=['POST'])
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