from __future__ import annotations
from typing import List
from pathlib import Path
import json

# from .... import constants
from .Novel import Novel
from . import database
from . import read_novel_info
import constants
from . import datetools

LIGHTNOVEL_FOLDER = Path(constants.DEFAULT_OUTPUT_PATH)
COMMENT_FOLDER = LIGHTNOVEL_FOLDER.parent / "Comments"

if not LIGHTNOVEL_FOLDER.exists():
    LIGHTNOVEL_FOLDER.mkdir()

if not COMMENT_FOLDER.exists():
    COMMENT_FOLDER.mkdir()

config = {"host": "localhost", "port": "5000", "website_url": "localhost:5000"}
# config_file = Path("lncrawl/bots/web/config.json")
# if not config_file.exists():
#     with open(config_file, "w", encoding="utf-8") as f:
#         json.dump({"host": "localhost", "port":"5000", "website_url":"localhost:5000"}, f, indent=4)
# with open(config_file, "r", encoding="utf-8") as f:
#     config = json.load(f)

WEBSITE_URL = config["website_url"]
HOST = config["host"]
PORT = config["port"]
WEBSITE_URL = WEBSITE_URL.strip("/")


database.all_novels: List[Novel] = []
for novel_folder in LIGHTNOVEL_FOLDER.iterdir():
    if novel_folder.is_dir():
        database.all_novels.append(read_novel_info.get_novel_info(novel_folder))

database.all_novels.sort(key=lambda x: sum(x.clicks.values()), reverse=True)
for i, n in enumerate(database.all_novels, start=1):
    n.rank = i

import datetime


database.sorted_all_novels = {
    "title": lambda: sorted(database.all_novels, key=lambda x: x.title),
    "author": lambda: sorted(database.all_novels, key=lambda x: x.author),
    "rating": lambda: sorted(
        database.all_novels, key=lambda x: x.overall_rating, reverse=True
    ),
    "views": lambda: sorted(
        database.all_novels, key=lambda x: sum(x.clicks.values()), reverse=True
    ),
    "weekly_views": lambda: sorted(
        database.all_novels,
        key=lambda x: x.clicks[datetools.current_week()]
        if datetools.current_week() in x.clicks
        else 0,
        reverse=True,
    ),
    "rank": lambda: database.all_novels,  # Default sort
    "last_updated": lambda: sorted(
        [
            source
            for novel in database.all_novels
            for source in novel.sources
            if source.last_update_date
        ],
        key=lambda x: datetime.datetime.fromisoformat(x.last_update_date),
        reverse=True,
    ),
    "title-reverse": lambda: database.sorted_all_novels["title"]()[::-1],
    "author-reverse": lambda: database.sorted_all_novels["author"]()[::-1],
    "rating-reverse": lambda: database.sorted_all_novels["rating"]()[::-1],
    "views-reverse": lambda: database.sorted_all_novels["views"]()[::-1],
    "weekly_views-reverse": lambda: database.sorted_all_novels["weekly_views"]()[::-1],
    "last_updated-reverse": lambda: database.sorted_all_novels["last_updated"]()[::-1],
}


import threading, time
import shutil
import sys


def update_novels_stats():
    """Periodic function to update each novels stats"""

    stopping = False
    while True:
        time.sleep(600)  # 10 minutes

        for novel in database.all_novels:
            # Security to avoid stopping the program while updating stats and having corrupted stats file
            # if KeyboardInterrupt or SystemExit is raised, finish the current loop then stop
            for attempt in range(4):
                try:
                    if not novel.path:
                        continue
                    stat_path = novel.path / "stats.json"

                    if not stat_path.exists():
                        shutil.copyfile("bots/web2/flask_api/_stats.json", stat_path)

                    with open(stat_path, "w", encoding="utf-8") as f:

                        novel_stats = {
                            "clicks": novel.clicks,
                            "ratings": novel.ratings,
                            "current_week_clicks": novel.current_week_clicks,
                        }

                        json.dump(novel_stats, f, indent=4)

                    print(f"Stats of {novel.title} updated")

                except KeyboardInterrupt or SystemExit:
                    stopping = True
                    continue

                break

            if stopping:
                sys.exit(0)

        print("Updated novels stats")


threading.Thread(target=update_novels_stats, daemon=True).start()
