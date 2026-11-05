import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen
from scripts.serve_demo import Handler


class WebServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def test_tasks_do_not_leak_labels(self):
        with urlopen(f'http://127.0.0.1:{self.port}/api/rank?budget=6') as f:
            data = json.load(f)
        self.assertEqual(len(data['tasks']), 10)
        self.assertLessEqual(data['spent_cost_units'], 6)
        self.assertTrue(all('critical_gap_label' not in x for x in data['tasks']))

    def test_context_explicitly_unavailable(self):
        with urlopen(f'http://127.0.0.1:{self.port}/api/context') as f:
            data = json.load(f)
        self.assertFalse(data['available'])

    def test_path_traversal_returns_404(self):
        with self.assertRaises(HTTPError) as cm:
            urlopen(f'http://127.0.0.1:{self.port}/data/synthetic/verification_tasks.json')
        self.assertEqual(cm.exception.code, 404)

    def test_invalid_budget_returns_400(self):
        with self.assertRaises(HTTPError) as cm:
            urlopen(f'http://127.0.0.1:{self.port}/api/rank?budget=-1')
        self.assertEqual(cm.exception.code, 400)


if __name__ == '__main__':
    unittest.main()
