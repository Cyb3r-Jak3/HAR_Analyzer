import json

import haralyzer
import pytest
from dotenv import load_dotenv
from flask.testing import FlaskClient

load_dotenv()


@pytest.fixture()
def har_file():
    with open("./tests/example.har") as infile:
        file = haralyzer.HarParser(json.load(infile))
    yield file


@pytest.fixture()
def har_page(har_file):
    yield har_file.pages[0]


@pytest.fixture()
def har_entry(har_page):
    yield har_page.entries[0]


class TestClient(FlaskClient):
    def __init__(self):
        load_dotenv()
        from app import app

        self.application = app
        self.application.testing = True
        super().__init__(application=self.application)


@pytest.fixture
def client():
    test_client = TestClient()
    ctx = test_client.application.app_context()
    ctx.push()
    yield test_client
    ctx.pop()


@pytest.fixture
def authed_client(client):
    with open("./tests/example.har", "rb") as infile:
        client.post(
            "/upload",
            data={"har_file": (infile, "example.har")},
            buffered=True,
            content_type="multipart/form-data",
            follow_redirects=True,
        )
    yield client
    client.get("/logout")
