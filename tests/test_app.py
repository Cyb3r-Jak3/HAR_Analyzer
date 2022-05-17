from app import allowed_file


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
    with open("./tests/example.har", "rb") as infile:
        file = infile.read()
    upload_resp = client.post("/upload", data={'har_file': (file, "example.har")})
    assert upload_resp.status_code == 302


