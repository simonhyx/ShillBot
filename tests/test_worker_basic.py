
import unittest
import codecs
import os

from workers.basic_worker import BasicUserParseWorker


class TestWorkerBasic(unittest.TestCase):

    def test_basic_worker_connection(self):
        """
        Purpose: Test regular running of worker
        Expectation: startup system, hit the reddit user and parse the data, fail to send to mothership (exception)

        :precondition: Mothership server not running
        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        # Can't connect to mother, so should raise ConnectionRefusedError, but should run everything else
        self.assertRaises(ConnectionRefusedError, worker.run)

    def test_worker_parsing(self):
        """
        Purpose: Test regular parsing mechanisms of worker
        Expectation: Load html file, send it to worker to parse, should return list of results

        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        file_path = '%s/%s' % (os.path.dirname(os.path.realpath(__file__)), 'test_resources/sample_GET_response.html')

        with codecs.open(file_path, encoding='utf-8') as f:
            text = f.read()

        results, next_page = worker.parse_text(str(text).strip().replace('\r\n', ''))

        self.assertGreater(len(results), 0)     # Check that results are returned
        self.assertEqual(len(results[0]), 3)    # Check that results are in triplets (check formatting)

    def test_worker_add_links_max_limit(self):
        worker = None
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        worker.max_links = 0
        len_to_crawl_before = len(worker.to_crawl)
        worker.add_links("test.com")
        len_to_crawl_after = len(worker.to_crawl)

        self.assertEqual(len_to_crawl_after, len_to_crawl_before)

    def test_worker_add_links_in_crawled(self):
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        worker.crawled = []

        len_to_crawl_before = len(worker.to_crawl)
        worker.add_links(["https://www.reddit.com/user/Chrikelnel"])
        len_to_crawl_after = len(worker.to_crawl)

        self.assertNotEqual(len_to_crawl_after, len_to_crawl_before)
        
    def test_worker_duplicate_links(self):
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        worker.crawled = []
        
        worker.add_links(["https://www.reddit.com/user/Chrikelnel"])
        worker.run()
        worker.add_links(["https://www.reddit.com/user/Chrikelnel"])
        len_after_adding_duplicate = len(worker.to_crawl)
        
        self.assertEqual(len_after_adding_duplicate, 0)
        
        
    def test_worker_run(self):
        len_crawled = len(worker.crawled)
        worker.run()
        len_crawled_after = len(worker.crawled)
        self.assertNotEqual(len_crawled, len_crawled_after)
        







