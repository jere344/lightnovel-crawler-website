from ..flaskapp import app
from flask import request
from .. import database
from .. import lib
from .Job import JobHandler, FinishedJob

# ----------------------------------------------- Search Novel ----------------------------------------------- #

@app.route("/api/addnovel/create_session")
@app.route("/addnovel/create_session")
def create_session():
    query = request.args.get("query")
    job_id = request.args.get("job_id")

    if not query:
        return {"status": "error", "message": "No query"}, 400
    if len(query) < 4:
        return {"status": "error", "message": "Query too short"}, 400

    if not job_id:
        return {"status": "error", "message": "No job_id"}, 400

    database.jobs[job_id] = job = JobHandler(job_id)

    job.get_list_of_novel(query)

    return {"status": "success"}, 200


# ----------------------------------------------- Choose Novel ----------------------------------------------- #

@app.route("/api/addnovel/get_novels_founds")
@app.route("/addnovel/get_novels_founds")
def get_novels_founds():
    """Return search results"""
    job_id = request.args.get("job_id")

    if not job_id in database.jobs:
        return {"status": "error", "message": "Job do not exist"}, 412

    job = database.jobs[job_id]

    if isinstance(job, FinishedJob):
        return {
            "status": "error",
            "message": f"Job aldready finished : {job.get_status()}",
        }, 409

    if job.is_busy:
        return {"status": "pending", "message": job.get_status()}, 202

    if not job.search_results:
        return {"status": "error", "message": "No search results"}, 404

    return {"status": "success", "novels": job.search_results}, 200


# ----------------------------------------------- Choose Source ----------------------------------------------- #

@app.route("/api/addnovel/get_sources_founds")
@app.route("/addnovel/get_sources_founds")
def get_sources_founds():
    """Return list of sources for selected novel"""
    job_id = request.args.get("job_id")
    novel_id = int(request.args.get("novel_id"))

    if not job_id in database.jobs:
        return {"status": "error", "message": "Job do not exist"}, 412

    job = database.jobs[job_id]
    if job.is_busy:
        return {"status": "pending", "message": job.get_status()}, 202

    if isinstance(job, FinishedJob):
        return {
            "status": "error",
            "message": f"Job aldready finished : {job.get_status()}",
        }, 409

    job.select_novel(novel_id)

    return {"status": "success", "sources": job.get_list_of_sources()}, 200


# ----------------------------------------------- Start Download ----------------------------------------------- #

@app.route("/api/addnovel/download")
@app.route("/addnovel/download")
def download():
    """Select Source and start download"""
    job_id = request.args.get("job_id")
    novel_id = int(request.args.get("novel_id"))
    source_id = int(request.args.get("source_id"))

    if not job_id in database.jobs:
        return {"status": "error", "message": "Job do not exist"}, 412

    job = database.jobs[job_id]
    if job.is_busy:
        return {"status": "pending", "message": job.get_status()}, 202

    if isinstance(job, FinishedJob):
        url = ""
        try:
            url = job.url
        except Exception as e:
            print("failed to get url : ", e)

        if job.success:
            return {
                "status": "success",
                "message": job.get_status(),
                "url": url,
            }, 200
        else:
            return {
                "status": "error",
                "message": job.get_status()
            }, 500

    if not job.metadata_downloaded:
        job.select_novel(novel_id)
        job.select_source(source_id)
        return {"status": "pending", "message": job.get_status()}, 202

    job.start_download()

    return {"status": "pending", "message": job.get_status()}, 202

    # Busy : Downloading metadata or downloading novel
    #    --> send status
    # Not busy :
    #    Job is finished :
    #        -> send status and url
    #    Metadata not downloaded :
    #       --> Select novel, select source (=> download metadata) --> busy
    #    Metadata downloaded :
    #       --> Start download --> busy


# ----------------------------------------------- Direct Download ----------------------------------------------- #

@app.route("/api/addnovel/direct_download")
@app.route("/addnovel/direct_download")
def direct_download():
    """Directly download a novel using the novel url"""

    job_id = request.args.get("job_id")

    novel_url = request.args.get("url")
    if not novel_url:
        return {"status": "error", "message": "Missing url"}, 400
    elif not novel_url.startswith("http"):
        return {"status": "error", "message": "Invalid URL"}, 400

    if not job_id in database.jobs or (
        isinstance(database.jobs[job_id], FinishedJob)
        and database.jobs[job_id].original_query != novel_url
    ):
        # If the job is finished and the query doesn't match, overwrite the old job
        database.jobs[job_id] = job = JobHandler(job_id)
    else:
        # If they match it means it is the current job, continue with it
        job = database.jobs[job_id]

    if job.is_busy:  # Job is busy
        return {"status": "pending", "message": job.get_status()}, 202

    elif isinstance(job, FinishedJob):  # job finished
        url = ""
        try:
            url = job.url
        except Exception as e:
            print(e)

        return {
            "status": "success",
            "message": job.get_status(),
            "url": url,
        }, 200

    elif not job.metadata_downloaded:  # job hasn't downloaded metadata yet
        job.prepare_direct_download(novel_url)
        return {"status": "pending", "message": job.get_status()}, 202

    else:  # job has downloaded metadata, isn't busy and isn't finished : start download
        job.start_download()
        return {"status": "pending", "html": job.get_status()}, 202


# ----------------------------------------------- Update ----------------------------------------------- #
import time
from threading import Thread
import datetime

@app.route("/api/addnovel/update")
@app.route("/addnovel/update")
def update():
    url = request.args.get("url")
    job_id = request.args.get("job_id")

    if job_id in database.jobs:
        job = database.jobs[job_id]
        if isinstance(job, FinishedJob):
            return {"status": "success", "message": job.get_status()}, 200
        else:
            return {"status": "pending", "message": job.get_status()}, 202
    else:
        # We check if it has aldreay been updated in the last hour
        job = [job for job in database.jobs.values() if job.original_query == url]
        if job:
            job = job[0]
            if isinstance(job, FinishedJob):
                if job.end_date + datetime.timedelta(hours=1) > datetime.datetime.now():
                    return {
                        "status": "error",
                        "message": "Novel aldready updating or recently updated",
                    }, 409

        Thread(target=_update, args=(url, job_id)).start()
        return {"status": "pending", "message": "Creating session"}, 202


import json
import datetime


def _update(url: str, job_id: str):
    job = database.jobs[job_id] = JobHandler(job_id)
    job.original_query = url
    job.prepare_direct_download(url)
    while job.is_busy:
        time.sleep(0.1)

    json_folder_path = lib.LIGHTNOVEL_FOLDER / job.novel_slug / job.source_slug / "json"

    no_new_chapters = True
    for chapter in job.app.crawler.chapters:
        chapter_path = json_folder_path / f"{str(chapter['id']).zfill(5)}.json"

        if chapter_path.exists():
            # We assume that if the body lenght is < 100 it was not downloaded correctly
            with open(str(chapter_path), "r", encoding='utf-8') as f:
                json_data = json.load(f)
            if len(json_data["body"]) < 100:
                print(f"Chapter {chapter['id']} is corrupted, redownloading it")
                # we simply delete the file for it to be re downloaded
                chapter_path.unlink()
                no_new_chapters = False

        else:
            no_new_chapters = False
                
    if no_new_chapters:
        job.set_last_action("No new chapters")
        job.destroy()
        return

    job.start_download()


# ----------------------------------------------- Load snapshot ----------------------------------------------- #
@app.route("/api/addnovel/load_snapshot")
@app.route("/addnovel/load_snapshot")
def load_snapshot():
    job_id = request.args.get("job_id")
    if job_id in database.jobs:
        job = database.jobs[job_id]
    else :
        print("Job not found")
        return {"status": "error", "message": "Invalid job_id"}, 400
        
    if not isinstance(job, FinishedJob):
        print("Job not finished")
        return {"status": "error", "message": "Job is not finished"}, 400
    
    if not job.snapshot_exists():
        print("Snapshot not found")
        return {"status": "error", "message": "No snapshot for this job"}, 400

    job.restore_snapshot()

    return {"status": "success", "message": "Snapshot loaded"}, 200
        
           