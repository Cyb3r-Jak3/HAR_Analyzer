from app import allowed_file
from io import StringIO


def test_allowed_file():
    assert allowed_file("file.jpg") is False
    assert allowed_file("example.har")


def test_index(client):
    assert client.get("/").status_code == 200


def test_about(client):
    assert client.get("/about").status_code == 200


def test_debug(client):
    resp = client.get("/debug")
    assert resp.status_code == 200
    assert resp.json["Redis"]


def test_upload(client):
    assert client.get("/upload").status_code == 200

    assert client.post("/upload").status_code == 302

    assert (
        client.post(
            "/upload",
            data={"har_file": (StringIO(""), "")},
            buffered=True,
            content_type="multipart/form-data",
            follow_redirects=True,
        ).status_code
        == 400
    )

    assert (
        client.post(
            "/upload",
            data={"har_file": (StringIO(""), "example.jpg")},
            buffered=True,
            content_type="multipart/form-data",
            follow_redirects=True,
        ).status_code
        == 400
    )
    with open("./tests/example.har", "rb") as infile:

        upload_resp = client.post(
            "/upload",
            data={"har_file": (infile, "example.har")},
            buffered=True,
            content_type="multipart/form-data",
            follow_redirects=True,
        )
    assert upload_resp.status_code == 200
    assert len(upload_resp.history) == 1
    assert upload_resp.request.path == "/report"


def test_entry_choice(authed_client):
    assert authed_client.get("/api/entry_choice").status_code == 405
    resp = authed_client.post("/api/entry_choice", json={"entry_id": 1})
    assert resp.status_code == 200


def test_no_redis(authed_client):
    authed_client.application.using_redis = False
    assert authed_client.get("/report").status_code == 200


# def test_no_file_report(authed_client):
#     with authed_client.session_transaction() as session:
#         session["filename"] = None
#     resp = authed_client.get("/report")
#     assert resp.status_code == 404


def test_no_file_logout(authed_client):
    with authed_client.session_transaction() as session:
        session["filename"] = None
    resp = authed_client.get("/logout")
    assert resp.status_code == 200
