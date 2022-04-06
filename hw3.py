from pathlib import Path
import argparse
from flask import Flask, render_template, request
from utils import load_wapo
from inverted_index import build_inverted_index, query_inverted_index
from mongo_db import db, insert_docs, query_doc

app = Flask(__name__)

MATCHES = []
SW = []
UNKNOWNS = []
QUERY = []

data_dir = Path(__file__).parent.joinpath("pa3_data")
wapo_path = data_dir.joinpath("wapo_pa3.jl")

if "wapo_docs" not in db.list_collection_names():
    # if wapo_docs collection is not existed, create a new one and insert docs into it
    insert_docs(load_wapo(wapo_path))


# home page
@app.route("/")
def home():
    return render_template("home.html")


# result page
@app.route("/results", methods=["GET", "POST"])
def results():
    # TODO:
    # clear past search info
    MATCHES.clear()
    SW.clear()
    UNKNOWNS.clear()
    QUERY.clear()

    query_text = request.form["query"]
    QUERY.append(query_text)
    result = query_inverted_index(query_text)

    matching_ids = result[0]
    SW.append(result[1])
    UNKNOWNS.append(result[2])

    # if query inverted index did not find any results
    if -1 in result[0]:
        return render_template("results.html", er="NOTHING FOUND: Make your query more informative!",
                               query_text=query_text, matches=MATCHES[:8], more_content="false",
                               url="results/", page_id=1, num_matches=len(MATCHES), stopwords=SW, unknown=UNKNOWNS)

    for doc_id in matching_ids:
        match = query_doc(doc_id)
        MATCHES.append([match['id'], match['title'], match['content_str'][:150]])

    if len(MATCHES) > 8:  # check if next page will be needed
        return render_template("results.html", er="", query_text=query_text, matches=MATCHES[:8], more_content="true",
                               url="results/2", page_id=1, num_matches=len(MATCHES), stopwords=SW, unknown=UNKNOWNS)
    else:
        return render_template("results.html", er="", query_text=query_text, matches=MATCHES, more_content="false",
                               page_id=2, num_matches=len(MATCHES), stopwords=SW, unknown=UNKNOWNS)


# "next page" to show more results
@app.route("/results/<int:page_id>", methods=["GET", "POST"])
def next_page(page_id):
    # TODO:
    if len(MATCHES) <= page_id * 8:
        return render_template("results.html", query_text=QUERY[0], matches=MATCHES[(page_id - 1) * 8:page_id * 8],
                               page_id=page_id + 1, more_content="false", num_matches=len(MATCHES),
                               stopwords=SW, unknown=UNKNOWNS)
    else:
        nextp = page_id + 1
        return render_template("results.html", query_text=QUERY[0], matches=MATCHES[(page_id - 1) * 8:page_id * 8],
                               page_id=page_id, more_content="true", url=f'{nextp}', num_matches=len(MATCHES),
                               stopwords=SW, unknown=UNKNOWNS)


# document page
@app.route("/doc_data/<int:doc_id>", methods=["GET", "POST"])
def doc_data(doc_id):
    # TODO:
    # get info to display on doc page
    doc = query_doc(doc_id)
    title = doc['title']
    author = doc['author']
    date = doc['published_date']
    to_display = doc['content_str']
    return render_template("doc.html", article=to_display, title=title, author=author, date=date)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Boolean IR system")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    if args.build:
        build_inverted_index(load_wapo(wapo_path))
    if args.run:
        app.run(debug=True, port=5000)
