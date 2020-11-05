from flask import abort, render_template, redirect, url_for, request, session, jsonify
from .har_worker import get_entries
import os
from functools import wraps
from uuid import uuid4
from .create_app import create_app

app = create_app()


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == "har"


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not app.config.get("REDIS_URL"):
            return f(*args, **kwargs)
        session_hash = session.get("filename")
        if session_hash is None:
            abort(404)
        if session_hash != app.redis_client.get(session.get("token").bytes).decode("utf-8"):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    return render_template("index.jinja")


@app.route("/about")
def about():
    return render_template("about.jinja")


@app.route("/debug")
def session_info():
    return jsonify(
        {
            "Session Hash": session.get("hash"),
            "Session Filename": session.get("filename"),
            "Version": app.config.get("VERSION"),
            "Redis": True if os.getenv("REDIS_URL") else False,
            "Git HASH": os.getenv("HEROKU_SLUG_COMMIT", None)
        }
    )


@app.route("/report")
@require_auth
def report():
    if not session.get("filename"):
        return render_template("error.jinja", message="No file was given"), 400
    return render_template("results.jinja", items=get_entries(session["filename"]))


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        if 'har_file' not in request.files:
            return redirect(request.url)
        file = request.files['har_file']
        if file.filename == '':
            return render_template("error.jinja", message="No File upload"), 400
        if file and allowed_file(file.filename):
            session["filename"] = app.hashing.hash_value(file.read(), salt=app.secret_key)
            file.stream.seek(0)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], session["filename"]))
            file.close()
            if app.config.get("REDIS_URL"):
                session["token"] = uuid4()
                app.redis_client.set(session["token"].bytes, session["filename"])
            return redirect(url_for("report"))
    return render_template("upload.jinja")


@app.route("/api/entry_choice", methods=["POST"])
@require_auth
def entry_choice():
    return dict(get_entries(session.get("filename"), request.get_json()["entry_id"]))


@app.route("/logout", methods=["GET"])
def logout():
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], session["filename"]))
        if app.config.get("REDIS_URL"):
            app.redis_client.delete(session["token"].bytes)
        session.clear()
        return render_template(
            "logout.jinja",
            message="Your session has been ended and the file has been removed from the server")
    except KeyError:
        return render_template(
            "logout.jinja",
            message="There was no session to end"
        )


@app.errorhandler(400)
def bad_request_error(e):
    return render_template("error.jinja", message=e), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.jinja", message=e), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error.jinja", message=e), 500


if __name__ == '__main__':
    app.run()
