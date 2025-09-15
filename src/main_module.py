#!/usr/bin/env python3
"""
@author: Marek Putala

"""

# libraries

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
import queue
from queue import Full, Empty
import requests
import sys

# set up max queue size (great if queue size balloons.)

MAX_QUEUE_SIZE = 100
# global for output web data

OUTPUT = []
# some testing urls, if someone runs swle_module without main run skript

TEST_URLS = ["https://example.com", "https://httpbin.org/get", "https://www.python.org"]

# creating queue used by concurrent threads for responses

q = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# function for concurrent url fetching


def fetch(url):
    # without timeout or bad url, theres happy-flow

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        try:
            q.put_nowait(response)
        except Full:
            # if queue is full, remove the oldest item and add the new response.

            try:
                removed = q.get_nowait()
                #print(f"Removed oldest item: {removed}")
                q.put_nowait(response)
            except Empty:
                # rarer case, if queue was full but emptied in the meantime

                print("Queue was empty, couldn't trim.")
                q.put_nowait(response)
    # if theres a timeout or bad url, url fetching is unsuccessful and process is terminated

    except requests.exceptions.RequestException as e:
        print(f"Exception occurred while fetching {url}: {e}")


def producer(urls):
    # each URL is fetched in its own dedicated thread.

    threads = []
    for u in urls:
        t = threading.Thread(target=fetch, args=(u,))
        t.start()
        threads.append(t)
    # after all URLs have been fetched, the producer continues.

    for t in threads:
        t.join()
    # the producer signals the consumer that all tasks are complete.

    q.put(None)
    #print("Producent is done! :)")


def consumer():
    # consumer loops until the producer indicates the queue is complete.

    while True:
        task = q.get()
        # if theres end signal, consumer has finished

        if task is None:
            #print("Consumer is done! :)")
            break
        #print("Consumer eats", task.url)
        # parsing HTML using BeautifulSoup library functions.

        soup = BeautifulSoup(task.text, "html.parser")
        links = []
        # skip empty or non-HTTP links (anchors, JavaScript, mailto, tel, file)

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if (
                href == ""
                or href.startswith("#")
                or href.startswith("javascript:")
                or href.startswith("mailto:")
                or href.startswith("tel:")
                or href.startswith("file:")
            ):
                continue
            # if a relative URL is found, it is converted to an absolute URL.

            absolute_url = urljoin(task.url, href)
            # all absolute URLs are collected into an array.

            links.append(absolute_url)
        OUTPUT.append((task.url, links))


def main(urls):
    # setting up threads for concurrent execution

    t1 = threading.Thread(target=producer, args=(urls,))
    t2 = threading.Thread(target=consumer)

    # starting threads

    t1.start()
    t2.start()

    # wait for all threads to complete

    t1.join()
    t2.join()

    # return all tuples of the form (main_url, [all found URLs])

    return OUTPUT


if __name__ == "__main__":
    main(TEST_URLS)
