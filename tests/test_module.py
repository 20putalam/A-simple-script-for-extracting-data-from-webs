#!/usr/bin/env python3
"""
@author: Marek Putala

"""

# libraries

import unittest
from src.main_module import fetch, q, MAX_QUEUE_SIZE, producer, OUTPUT, consumer
from unittest.mock import patch, MagicMock
import requests
import queue

# test cases for the fetch function

class TestFetch(unittest.TestCase):

    # test that fetch() successfully retrieves a response and puts it in the queue

    @patch("requests.get")
    def test_fetch_success_put_in_queue(self, mock_get):
        """Inserting response in queue"""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        q.queue.clear()

        fetch("http://example.com")

        self.assertEqual(q.qsize(), 1)
        self.assertIs(q.get(), mock_response)

    # test that fetch() correctly handles insertion into a full queue.

    @patch("requests.get")
    def test_fetch_success_put_in_full_queue(self, mock_get):
        """Inserting response in full queue"""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        q.queue.clear()

        q.put(1)
        for i in range(MAX_QUEUE_SIZE - 1):
            q.put(0)
        self.assertEqual(q.queue[0], 1)
        self.assertEqual(q.queue[1], 0)
        self.assertEqual(q.qsize(), 100)
        fetch("https://example.com")
        self.assertEqual(q.queue[0], 0)
        self.assertEqual(q.queue[1], 0)
        self.assertEqual(q.qsize(), 100)

    # test that fetch() properly handles a timeout exception.

    @patch("requests.get")
    def test_fetch_timeout(self, mock_get):
        """Test fetch handles timeout exception."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        fetch("http://example.com")

        self.assertEqual(q.qsize(), 0)


# test cases for the producer function

class TestProducer(unittest.TestCase):

    # test the producer function in the happy path scenario.

    @patch("src.main_module.fetch")
    def test_producer_success(self, mock_fetch):
        """Test producer happy flow."""

        urls = ["http://example.com/1", "http://example.com/2", "http://example.com/3"]
        q.queue.clear()
        mock_fetch.side_effect = lambda url: q.put(f"response from {url}")
        producer(urls)
        expected_size = len(urls) + 1
        self.assertEqual(q.qsize(), expected_size)
        items = list(q.queue)
        self.assertEqual(items[-1], None)
        for i, url in enumerate(urls):
            self.assertEqual(items[i], f"response from {url}")


# test cases for the consumer function

class TestConsumerHappyFlow(unittest.TestCase):

    # test the consumer function in the happy path scenario.

    def test_consumer_happy_flow(self):
        q.queue.clear()
        OUTPUT.clear()
        task1 = MagicMock()
        task1.url = "http://example.com/page1"
        task1.text = """
        <html>
            <body>
                <a href="http://example.com/link1">Link 1</a>
                <a href="/relative/link2">Link 2</a>
                <a href="#ignore">Ignore me</a>
            </body>
        </html>
        """
        task2 = MagicMock()
        task2.url = "http://example.com/page2"
        task2.text = """
        <html>
            <body>
                <a href="http://example.com/link3">Link 3</a>
            </body>
        </html>
        """

        q.put(task1)
        q.put(task2)
        q.put(None)
        consumer()
        self.assertEqual(len(OUTPUT), 2)

        url1, links1 = OUTPUT[0]
        self.assertEqual(url1, "http://example.com/page1")
        self.assertIn("http://example.com/link1", links1)
        self.assertIn("http://example.com/relative/link2", links1)
        self.assertNotIn("#ignore", links1)

        url2, links2 = OUTPUT[1]
        self.assertEqual(url2, "http://example.com/page2")
        self.assertIn("http://example.com/link3", links2)


if __name__ == "__main__":
    unittest.main()
