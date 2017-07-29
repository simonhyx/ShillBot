
import unittest
import codecs
import os

from workers.basic_worker import BasicUserParseWorker
from mothership.base import MothershipServer


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
        len_initial = len(worker.to_crawl)
        
        worker.crawled.append("https://www.reddit.com/user/Chrikelnel")
        worker.add_links(["https://www.reddit.com/user/Chrikelnel"])
        len_after_adding_duplicate = len(worker.to_crawl)
        
        self.assertEqual(len_after_adding_duplicate, len_initial)
        
        
    def test_worker_init(self):
        abc = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        bcd = BasicUserParseWorker("https://www.afd.com/")
        sdf = BasicUserParseWorker("https://www.sdf.com/user/Chrikelnel2")
        link1 = abc.to_crawl[0]
        link = "https://www.reddit.com/user/Chrikelnel"
        self.assertEqual(link, link1)
        self.assertNotEqual(abc.to_crawl[0], sdf.to_crawl[9])
        self.assertNotEqual(bcd.to_crawl[0], sdf.to_crawl[9])

    def test_worker_max_links(self):

        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        
        worker.add_links(["https://www.reddit.com/user/Chrikelnel"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel1"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel2"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel3"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel4"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel5"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel6"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel7"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel8"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel9"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel10"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel11"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel12"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel13"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel14"])
        worker.add_links(["https://www.reddit.com/user/Chrikelnel15"])
        len_after = len(worker.crawled)
        self.assertNotEqual(len_after, 10)
        
        







