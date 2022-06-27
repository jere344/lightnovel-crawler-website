from ..flaskapp import app
from flask import redirect, render_template, request, send_from_directory
from .. import lib
from urllib.parse import unquote_plus
import json
from math import ceil
import difflib

@app.route("/lncrawl/")
@app.route("/lncrawl/page-<int:page>")
def menu(page=None):
    """
    Main page of the web interface.
    Displays all downloaded novels in a random order.

    #TODO : order by the most clicked novels
    """
    last_page = ceil(len(lib.all_downloaded_novels) / 50)
    start = ((page if page else 1) - 1) * 50
    stop = min((page if page else 1) * 50, len(lib.all_downloaded_novels))

    return render_template(
        "reader/menu.html",
        novels=lib.all_downloaded_novels[start:stop],
        page=page,
        last_page=last_page,
    )


@app.route("/lncrawl/novel/<path:novel_and_source_path>/chapterlist/")
@app.route("/lncrawl/novel/<path:novel_and_source_path>/chapterlist/page-<int:page>")
def chapterlist(novel_and_source_path, page=None):
    """
    Displays the list of chapters for the novel with selected source.
    """

    novel_and_source_path = lib.LIGHTNOVEL_FOLDER / unquote_plus(novel_and_source_path)
    novel = lib.get_source_info(novel_and_source_path)

    with open(novel_and_source_path / "meta.json", "r", encoding="utf-8") as f:
        chapters = json.load(f)["chapters"]
        start = ((page if page else 1) - 1) * 100
        stop = min((page if page else 1) * 100, len(chapters))
        chapters = chapters[start:stop]

    return render_template(
        "reader/chapterlist.html",
        novel=novel,
        chapters=chapters,
        page=page,
        last_page=ceil(novel.chapter_count / 100),
    )


@app.route("/lncrawl/novel/<path:novel_and_source_path>/gotochap", methods=["POST"])
def gotochap(novel_and_source_path):
    """
    POST method to redirect to a chapter
    Need form input "chapno"
    
    => Redirect to the chapter id in the form input "chapno"
    """
    return redirect(
        f"/lncrawl/novel/{novel_and_source_path}/chapter-{request.form.get('chapno')}"
    )


@app.route("/lncrawl/novel/<path:novel_and_source_path>/")
def novel_info(novel_and_source_path):
    """
    Show the info page for a novel.
    """
    novel_and_source_path = lib.LIGHTNOVEL_FOLDER / unquote_plus(novel_and_source_path)

    source = lib.findSourceWithPath(novel_and_source_path)

    return render_template(
        "reader/novel_info.html",
        source=source,
        len_sources=len(source.novel.sources)

    )


@app.route("/lncrawl/novel/<path:novel_and_source_path>/chapter-<int:chapter_id>")
def chapter(novel_and_source_path, chapter_id: int):
    """
    Display a chapter.
    """
    novel_and_source_path = lib.LIGHTNOVEL_FOLDER / unquote_plus(novel_and_source_path)
    chapter_folder = novel_and_source_path / "json"

    chapter_file = chapter_folder / f"{str(chapter_id).zfill(5)}.json"
    prev_chapter = chapter_folder / f"{str(chapter_id - 1).zfill(5)}.json"
    next_chapter = chapter_folder / f"{str(chapter_id + 1).zfill(5)}.json"

    with open(chapter_file, encoding="utf8") as f:
        chapter = json.load(f)

    source = lib.findSourceWithPath(novel_and_source_path)

    return render_template(
        "reader/chapter.html",
        chapter=chapter,
        is_prev=prev_chapter.exists(),
        is_next=next_chapter.exists(),
        source=source,
    )

@app.route("/lncrawl/novel/<path:novel_and_source_path>/images/<string:image_name>/")
def novel_image(novel_and_source_path, image_name:str):
    """
    Allow to load an image from the novel as linked in json content.
    """
    file = f"{unquote_plus(novel_and_source_path)}/images/{image_name}"
    path = lib.LIGHTNOVEL_FOLDER / file
    if path.exists():
        return send_from_directory(lib.LIGHTNOVEL_FOLDER, file)
    else:
        print(path)
        print(path.name)


@app.route("/lncrawl/lnsearchlive", methods=["POST"])
def lnsearchlive():
    """
    POST method for live search
    Need form input "inputContent"

    => return a list of max 20 best matches from downloaded novels
    """

    search_query = lib.sanitize(request.form.get("inputContent").replace("+", " ")).split(" ")
    ratio = []
    for downloaded in lib.all_downloaded_novels:
        count = 0
        for search_word in search_query:
            count += len(difflib.get_close_matches(search_word, downloaded.search_words))
        ratio.append((downloaded, count))

    ratio.sort(key=lambda x: x[1], reverse=True)

    number_of_results = min(20, len(lib.all_downloaded_novels))

    search_results = [novel for novel, ratio in ratio[: number_of_results] if ratio != 0]

    return {
        "$id": "1",
        "success": True,
        "resultview": render_template(
            "reader/lnsearchlive.html", novels=search_results
        ),
    }


@app.route("/lncrawl/search")
def search():
    """
    Return the search page.
    """
    return render_template("reader/search.html")
