from typing import Dict, Union, Generator
import functools
import os
import time
import json
import re
from datetime import datetime


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_t = time.perf_counter()
        f_value = func(*args, **kwargs)
        elapsed_t = time.perf_counter() - start_t
        mins = elapsed_t // 60
        print(
            f"'{func.__name__}' elapsed time: {mins} minutes, {elapsed_t - mins * 60:0.2f} seconds"
        )
        return f_value

    return wrapper_timer


CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def load_wapo(wapo_jl_path: Union[str, os.PathLike]) -> Generator[Dict, None, None]:
    """
    Unlike HW2, load_wapo should be an iterator in this assignment. It's more memory-efficient when you need to
    load each document and build the inverted index.
    At each time, load_wapo will yield a dictionary of the following format:

    {
        "id": 1,
        "title": "Many Iowans still don't know who they will caucus for",
        "author": "Jason Horowitz",
        "published_date": 2011-12-31 20:37:52,
        "content_str": "Iran announced a nuclear fuel breakthrough and test-fired ..."
      }
    Compared to HW2, you should also make the following changes:
    - replace the original value of the key "id" with an integer that corresponds to the order of each document
      that has been loaded. For example. the id of the first yielded document is 0 and the second is 1 and so on.
    - remove any HTML elements from the content_str.
    - convert the value of "published_date" to a readable format.
      This one is given as follows, so just sure you apply it in your implementation
            %: from datetime import datetime
            %: doc["published_date"] = datetime.fromtimestamp(doc["published_date"] / 1000.0)

    :param wapo_jl_path:
    :return:
    """
    # TODO:

    idx = 0  # counter for article id
    data = []  # list to hold json lines
    for json_line in open(wapo_jl_path):
        data.append(json.loads(json_line))  # append json line to list

    for article in data:
        content_str = ""
        for content in article["contents"]:
            if content is not None:
                if content["type"] == "sanitized_html":
                    content_str += " " + content["content"]

        article_dict = {"id": idx,
                        "title": article["title"],
                        "author": article["author"],
                        "published_date": datetime.fromtimestamp(article["published_date"] / 1000.0).strftime(
                            '%m/%d/%Y'),
                        "content_str": cleanhtml(content_str)}
        idx += 1
        yield article_dict


if __name__ == "__main__":
    docs = load_wapo("small_wapo.jl")
    [print(doc) for doc in docs]
