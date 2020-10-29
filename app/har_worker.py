import json
import os
from haralyzer_3 import HarParser, HarPage


def mimeType_splitter(mime_type: str) -> str:
    raw_type = mime_type
    if raw_type.find(";"):
        raw_type = raw_type.split(";")[0]
    return raw_type.split("/")[1]


def create_request_count(page: HarPage, attribute: str) -> dict:
    results = {}
    for entry in page.entries:
        item = getattr(entry.request, attribute)
        if item in results.keys():
            results[item] += 1
        else:
            results[item] = 1

    return results


def create_response_count(page: HarPage, attribute: str) -> dict:
    results = {}
    for entry in page.entries:
        item = getattr(entry.response, attribute)
        if attribute == "mimeType":
            item = mimeType_splitter(item)
        if item in results.keys():
            results[item] += 1
        else:
            results[item] = 1

    return results


def create_root_count(page: HarPage, attribute: str) -> dict:
    results = {}
    for entry in page.entries:
        item = getattr(entry, attribute)
        if item in results.keys():
            results[item] += 1
        else:
            results[item] = 1

    return results


def get_entries(filename: str, entry_id: int = None) -> (dict, list):
    with open(os.path.join(os.getenv("UPLOAD_FOLDER", "./uploads"), filename), 'r') as process_file:
        render_pages = HarParser(json.loads(process_file.read())).pages
    items = [entry for page in render_pages for entry in page.entries]
    if isinstance(entry_id, int):
        return items[entry_id]
    return items
