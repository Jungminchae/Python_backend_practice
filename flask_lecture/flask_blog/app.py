import os
from flask import Flask, jsonify, request, render_template, make_response
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_cors import CORS

# https 만을 지원하는 기능을 http에서 테스트할 때 필요한 설정
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__, static_url_path="/static")
CORS(app)
# 실제로는 secure_key는 보안을 높이기 위해 랜덤한 값을 넣어줌
# Django secret key 생각하면 될 듯
app.secure_key = "mc_server"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"  # session을 보다 복잡하게


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
