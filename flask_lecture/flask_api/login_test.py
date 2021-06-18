from flask import Flask, jsonify, request, render_template

app = Flask(__name__, static_url_path="/static")


@app.route("/login")
def login():
    if username := request.args.get("user_name") == "M":
        return_data = {"auth": "success"}
    else:
        return_data = {"auth": "failed"}
    return jsonify(return_data)


@app.route("/login_test")
def login_test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080")
