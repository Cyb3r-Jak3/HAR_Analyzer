"""File that deals with all the Har files and parsing"""
import json
import os
from haralyzer import HarParser, HarPage


def mimetype_splitter(mime_type: str) -> str:
    """Returns the mimetype of the content"""
    raw_type = mime_type
    if raw_type.find(";"):
        raw_type = raw_type.split(";")[0]
    return raw_type.split("/")[1]


def create_request_count(page: HarPage, attribute: str) -> dict:
    """Gets all the request content"""
    results = {}
    for entry in page.entries:
        item = getattr(entry.request, attribute)
        if item in results.keys():
            results[item] += 1
        else:
            results[item] = 1

    return results


def create_response_count(page: HarPage, attribute: str) -> dict:
    """Gets all the response content"""
    results = {}
    for entry in page.entries:
        item = getattr(entry.response, attribute)
        if attribute == "mimeType":
            item = mimetype_splitter(item)
        if item in results.keys():
            results[item] += 1
        else:
            results[item] = 1

    return results


def create_root_count(page: HarPage, attribute: str) -> dict:
    """Get the count of the root entry info"""
    results = {}
    for entry in page.entries:
        item = getattr(entry, attribute)
        if item in results.keys():
            results[item] += 1
        else:
            results[item] = 1

    return results


def get_entries(filename: str, entry_id: int = None) -> (dict, list):
    """Gets either all the entries or a certain one"""
    with open(
        os.path.join(os.getenv("UPLOAD_FOLDER", "/tmp"), filename), "r"  # nosec
    ) as process_file:
        render_pages = HarParser(json.loads(process_file.read())).pages
    items = [entry for page in render_pages for entry in page.entries]
    if isinstance(entry_id, int):
        return items[entry_id]
    return items
