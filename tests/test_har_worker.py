import os

from app import har_worker
from haralyzer import HarEntry


def test_mimetype_splitter():
    without_encoding = har_worker.mimetype_splitter("application/json")
    assert without_encoding == "json"

    with_encoding = har_worker.mimetype_splitter("application/json; charset=utf-8")
    assert with_encoding == "json"


def test_create_request_count(har_page):
    count = har_worker.create_request_count(har_page, "url")
    assert isinstance(count, dict)
    assert len(count) == 31


def test_create_response_count(har_page):
    count = har_worker.create_response_count(har_page, "httpVersion")
    assert isinstance(count, dict)
    assert len(count) == 1


def test_create_root_count(har_page):
    count = har_worker.create_root_count(har_page, "pageref")
    assert isinstance(count, dict)
    assert len(count) == 1


def test_get_entries():
    os.environ["UPLOAD_FOLDER"] = "./tests"
    entries = har_worker.get_entries("example.har")
    assert len(entries) == 34
    first = entries[0]
    assert isinstance(first, HarEntry)
    assert first.url == "https://cyberjake.xyz/"

    entry = har_worker.get_entries("example.har", 2)
    assert isinstance(entry, HarEntry)
    assert entry.url == "https://cyberjake.xyz/css/main.css"
