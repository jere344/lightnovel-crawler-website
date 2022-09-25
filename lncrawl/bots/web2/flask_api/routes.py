from flask import request, send_from_directory
from . import lib
from . import flaskapp
from . import database
from . import utils
import pathlib
import math
from urllib.parse import unquote_plus
import json
from typing import List
from .Novel import Novel, NovelFromSource
import difflib
from . import sanatize


@flaskapp.app.route("/api/image/<path:file>")
def image(file: pathlib.Path):
    path: pathlib.Path = lib.LIGHTNOVEL_FOLDER / file
    if path.exists():
        return send_from_directory(lib.LIGHTNOVEL_FOLDER, file), 200
    else:
        print(path)
    return "", 404


@flaskapp.app.route("/api/flags/<string:language>")
def flags(language: str):
    if not len(language) == 2:
        return "", 404

    return send_from_directory("static/flags", language + ".svg"), 200


# /api/novels?page=${page}
@flaskapp.app.route("/api/novels")
def get_novels():
    """
    :number: The number of novels to return / the number of novel per page
    :page: Page number
    :sort: Sort by [rank, views, title, author, rating] (default: rank)

    """
    page = request.args.get("page")
    if not page:
        page = 0

    number = request.args.get("number")
    if not number:
        number = 20

    sort = request.args.get("sort")
    if not sort:
        sort = "rank"

    page = int(page)
    number = int(number)

    start = page * number
    stop = (page + 1) * number
    content = {
        (page * number + 1 + i): e.asdict()
        for i, e in enumerate(database.sorted_all_novels[sort]()[start:stop])
    }
    return {
        "content": content,
        "metadata": {
            "total_pages": math.ceil(len(database.all_novels) / number),
            "current_page": page,
        },
    }, 200


from . import datetools


@flaskapp.app.route("/api/novel")
def get_novel():
    novel_slug = request.args.get("novel")
    source_slug = request.args.get("source")
    if not novel_slug or not source_slug:
        return "", 404

    source_path = (
        lib.LIGHTNOVEL_FOLDER / unquote_plus(novel_slug) / unquote_plus(source_slug)
    )
    if not source_path.exists():
        return "", 404
    source = utils.find_source_with_path(source_path)
    if not source:
        return "", 404

    current_week = datetools.current_week()
    if current_week not in source.novel.clicks:
        source.novel.clicks[current_week] = 0

    source.novel.clicks[current_week] += 1

    return source.asdict(), 200


@flaskapp.app.route("/api/chapter/")
def get_chapter():
    novel_slug = request.args.get("novel")
    source_slug = request.args.get("source")
    chapter_id = request.args.get("chapter")
    if not novel_slug or not source_slug or not chapter_id:
        return "invalid request : novel, source or chapter missing", 400
    chapter_folder = (
        lib.LIGHTNOVEL_FOLDER
        / unquote_plus(novel_slug)
        / unquote_plus(source_slug)
        / "json"
    )
    chapter_path = chapter_folder / f"{str(chapter_id).zfill(5)}.json"
    if not chapter_path.exists():
        return "", 404

    with open(chapter_path, "r", encoding='utf-8') as f:
        chapter = json.load(f)

    if not chapter_path.exists():
        return "", 404

    is_next = (chapter_folder / f"{str(int(chapter_id) + 1).zfill(5)}.json").exists()
    is_prev = (chapter_folder / f"{str(int(chapter_id) - 1).zfill(5)}.json").exists()

    source = utils.find_source_with_path(chapter_folder.parent)

    current_week = datetools.current_week()
    if current_week not in source.novel.clicks:
        source.novel.clicks[current_week] = 0

    source.novel.clicks[current_week] += 1

    return {
        "content": chapter,
        "is_next": is_next,
        "is_prev": is_prev,
        "source": source.asdict(),
    }, 200


@flaskapp.app.route("/api/chapterlist/")
def get_chapter_list():
    novel_slug = request.args.get("novel")
    source_slug = request.args.get("source")
    page = request.args.get("page")
    if not novel_slug or not source_slug or not page:
        return "invalid request : novel or source missing", 400
    page = int(page) - 1

    meta_file = (
        lib.LIGHTNOVEL_FOLDER
        / unquote_plus(novel_slug)
        / unquote_plus(source_slug)
        / "meta.json"
    )

    source = utils.find_source_with_path(meta_file.parent)
    current_week = datetools.current_week()
    if current_week not in source.novel.clicks:
        source.novel.clicks[current_week] = 0

    source.novel.clicks[current_week] += 1

    with open(meta_file, "r", encoding='utf-8') as f:
        chapter_list = json.load(f)["chapters"]

    start = page * 100
    stop = min((page + 1) * 100, len(chapter_list) + 1)

    is_next = (page + 1) * 100 < len(chapter_list)
    is_prev = page > 0
    total_pages = math.ceil(len(chapter_list) / 100)

    return {
        "content": chapter_list[start:stop],
        "source": source.asdict(),
        "is_next": is_next,
        "is_prev": is_prev,
        "total_pages": total_pages,
    }, 200


@flaskapp.app.route("/api/search/")
def search():
    """
    => return a list of max 20 best matches from downloaded novels
    """
    query = request.args.get("query")

    if not query or len(query) < 3:
        return "Invalid query", 400

    query = sanatize.sanitize(query).split(" ")
    ratio: List[tuple[Novel, int]] = []
    for downloaded in database.all_novels:
        count = 0
        for search_word in query:
            count += len(
                difflib.get_close_matches(search_word, downloaded.search_words)
            )
        ratio.append((downloaded, count))

    ratio.sort(key=lambda x: x[1], reverse=True)

    number_of_results = min(20, len(database.all_novels))

    search_results = [
        novel.asdict() for novel, ratio in ratio[:number_of_results] if ratio != 0
    ]

    return {
        "content": search_results,
        "results": number_of_results,
    }, 200


@flaskapp.app.route("/api/rate", methods=["POST"])
def rate():

    data = request.get_json()

    novel_slug = data.get("novel")
    rating = int(data.get("rating"))

    if not 0 < rating < 6:
        return {"status": "error", "message": "Rating must be between 1 and 5"}, 400

    novel = utils.get_novel_with_slug(novel_slug)

    novel.ratings[utils.shuffle_ip(request.remote_addr)] = rating

    return {"status": "success", "message": "Rating added"}, 200
